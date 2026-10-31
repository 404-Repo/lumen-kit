from __future__ import annotations

import base64
import io

from PIL import Image
from witness_client import AsyncWitnessClient, RenderOptions

SHEET = ((30, 0), (330, 0), (0, -30), (90, 0))
VIEW_PX = 512


def grid_options(pairs, px: int) -> RenderOptions:
    thetas, phis = [t for t, _ in pairs], [p for _, p in pairs]
    return RenderOptions(thetas=tuple(float(t) for t in thetas), phis=tuple(float(p) for p in phis),
                         img_size=px, bg_color="ffffff", lighting="neutral", cam_radius=2.0,
                         cam_fov_deg=49.1, gap=0)


async def _sheet(witness, source: str, pairs, px: int) -> bytes:
    im = Image.open(io.BytesIO(await witness.render(source, grid_options(pairs, px)))).convert("RGB")
    if im.size != (2 * px, 2 * px):
        gap = im.size[0] - 2 * px
        if im.size[0] == im.size[1] and gap > 0:
            canvas = Image.new("RGB", (2 * px, 2 * px), (255, 255, 255))
            for i in range(len(pairs)):
                x, y = (i % 2) * (px + gap), (i // 2) * (px + gap)
                canvas.paste(im.crop((x, y, x + px, y + px)), ((i % 2) * px, (i // 2) * px))
            im = canvas
        else:
            im = im.resize((2 * px, 2 * px), Image.Resampling.BILINEAR)
    buf = io.BytesIO()
    im.save(buf, format="PNG", compress_level=6)
    return buf.getvalue()


async def sheet(witness: AsyncWitnessClient, source: str) -> bytes:
    return await _sheet(witness, source, SHEET, VIEW_PX)


FRONT = ((30, 0), (330, 0), (0, 15), (0, -30))
FRONT_PX = 384


async def front_sheet(witness: AsyncWitnessClient, source: str) -> bytes:
    return await _sheet(witness, source, FRONT, FRONT_PX)


def data_url(png: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(png).decode("ascii")
