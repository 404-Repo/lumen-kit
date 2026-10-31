from witness_client import AsyncWitnessClient

from sn17gen.pipeline import run


async def generate(image: bytes, seed: int, witness: AsyncWitnessClient) -> str | None:
    return await run(image, seed, witness)
