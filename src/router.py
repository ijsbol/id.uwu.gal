from http import HTTPStatus
import io

import cv2
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse

from identicon import generate_identicon


# This is to tell redoc that we're returning an image/png.
class IdenticonStreamingResponse(FileResponse):
    media_type = 'image/png'



with open('../.git/FETCH_HEAD', 'r') as f:
    recent_git_commit_hash = f.read().split('	')[0][:8]


app = FastAPI(
    title="ID.UWU.GAL",
    version=recent_git_commit_hash,
    redoc_url="/docs",
    docs_url=None,
)


@app.get(path="/", include_in_schema=False)
async def main_page() -> RedirectResponse:
    return RedirectResponse(url="https://git.uwu.gal/id.uwu.gal")


@app.get(
    path="/i",
    status_code=HTTPStatus.OK,
    description="Generate an identicon for a provided identity string.",
    response_class=IdenticonStreamingResponse,
)
async def generate_identity(
    id: str = Query(
        default="hello, world",
        title="Identity",
        description="The string you wish to generate an identicon for.",
    ),
    size: int = Query(
        default=7,
        ge=4,
        le=8,
        title="Size",
        description="The pixel-width of the generated identicon.",
    ),
    scale: int = Query(
        default=40,
        ge=1,
        le=40,
        title="Scale",
        description="The scale factor to multiply the pixel-size by.",
    ),
) -> StreamingResponse:
    identity_image = generate_identicon(id, size=size, scale=scale)
    _, img_encoded = cv2.imencode('.png', identity_image)
    img_byte_arr = io.BytesIO(img_encoded.tobytes())

    return StreamingResponse(
        content=img_byte_arr,
        media_type="image/png",
        status_code=HTTPStatus.OK,
    )
