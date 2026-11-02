import asyncio
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

import httpx
from bittensor_wallet import Wallet
from miner_runtime.batch import run
from subnet_common.competition.generations import GenerationsAdapter

from main import generate

WALLET = "validator"
HOTKEY = "tensorplex"
CDN = "https://subnet404.xyz"
REF = "bf0b8ddbae743b86244f55cadcc83d94a50aa5a5"
PROMPTS_URL = (
    f"https://raw.githubusercontent.com/404-Repo/"
    f"404-active-competition/{REF}/rounds/1/prompts.txt"
)
OUTPUT = Path(
    "/Users/maximbladyko/atlas/404-active-competition/"
    "rounds/1/leader/generated.json"
)
CONFIG = Path("/private/tmp/lumen-kit-witness.json")
CONFIG.write_text(json.dumps({
    "witness_url": "https://witness.subnet404.xyz",
    "proof_parameters":
        "/Users/maximbladyko/atlas/404-base-miner/proof-parameters",
}))

async def main():
    async with httpx.AsyncClient(
        timeout=30, follow_redirects=True, trust_env=False
    ) as http:
        response = await http.get(PROMPTS_URL)
        response.raise_for_status()
        urls = [line.strip() for line in response.text.splitlines() if line.strip()]
        prompts = {
            Path(unquote(urlsplit(url).path)).stem: url
            for url in urls
        }

        await run(
            generate, prompts, 3347385824,
            witness_config=CONFIG,
            wallet_name=WALLET,
            wallet_hotkey=HOTKEY,
            wallet_path="~/.atlas",
            workers=12,
            parallel_calls=12,
        )

        address = Wallet(name=WALLET, hotkey=HOTKEY, path=str(Path("~/.atlas").expanduser())).hotkey.ss58_address
        response = await http.get(
            f"{CDN}/rounds/gpt-1/{address}/submitted.json",
            headers={"Cache-Control": "no-cache"},
        )
        response.raise_for_status()
        results = GenerationsAdapter.validate_json(response.content)

        if set(results) != set(prompts):
            raise RuntimeError("Saved index does not match all 128 official prompts")

        for result in results.values():
            if not result.failure_reason and (
                result.js is None or result.views is None
            ):
                raise RuntimeError("Saved index contains an incomplete result")
            if result.js is not None:
                result.js = f"{CDN}/{result.js}"
            if result.views is not None:
                result.views = f"{CDN}/{result.views}"

        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(GenerationsAdapter.dump_json(results, indent=2))
        print(f"Prepared {OUTPUT}")

asyncio.run(main())