import argparse
from io import BytesIO

import fastapi
from socaity_router import SocaityRouter, UploadDataType
from fastapi.responses import StreamingResponse
import cv2

import numpy as np

from face2face.settings import PORT, PROVIDER
from face2face.core.face2face import Face2Face

f2f = Face2Face()
router = SocaityRouter(
    provider=PROVIDER,
    app=fastapi.FastAPI(
        title="Face2Face FastAPI",
        summary="Swap faces from images. Create face embeddings. Integrate into hosted environments.",
        version="0.0.2",
        contact={
            "name": "SocAIty",
            "url": "https://github.com/SocAIty",
        }
    ),
)


async def upload_file_to_cv2(file: fastapi.UploadFile):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def cv2_to_bytes(img: np.ndarray):
    is_success, buffer = cv2.imencode(".png", img)
    io_buf = BytesIO(buffer)
    return io_buf


@router.add_route("/swap_one")
async def swap_one(source_img: UploadDataType.FILE, target_img: UploadDataType.FILE):
    source_img = await upload_file_to_cv2(source_img)
    target_img = await upload_file_to_cv2(target_img)

    swapped_img = f2f.swap_one_image(source_img, target_img)
    swapped_img = cv2_to_bytes(swapped_img)

    out_file_name = "swapped_img.png"

    return StreamingResponse(
        swapped_img,
        media_type="png",
        headers={"Content-Disposition": f"attachment; filename={out_file_name}"},
    )


@router.add_route("/add_reference_face")
async def add_reference_face(face_name: str, source_img: UploadDataType.FILE = None, save: bool = True):
    source_img = await upload_file_to_cv2(source_img)
    face_name, face_embedding = f2f.add_reference_face(
        face_name, source_img, save=save
    )

    return StreamingResponse(
        face_embedding,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={face_name}.npz"},
    )


@router.add_route("/swap_from_reference_face")
async def swap_from_reference_face(face_name: str, target_img: UploadDataType.FILE = None):
    target_img = await upload_file_to_cv2(target_img)
    swapped_img = f2f.swap_from_reference_face(face_name, target_img)
    swapped_img = cv2_to_bytes(swapped_img)

    return StreamingResponse(
        swapped_img,
        media_type="png",
        headers={
            "Content-Disposition": f"attachment; filename={face_name}_swapped.png"
        },
    )

def start_server(port: int = PORT):
    router.start(port=port)

# start the server on provided port
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--port", type=int, default=PORT)
    args = arg_parser.parse_args()
    start_server(port=args.port)
