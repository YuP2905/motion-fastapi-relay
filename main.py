from __future__ import annotations
from typing import (
    Annotated,
)
from fastapi import (
    FastAPI,
    Request,
    Depends,
    HTTPException
)
from fastapi.responses import (
    HTMLResponse,
    StreamingResponse,
)
from fastapi.staticfiles import (
    StaticFiles
)
from fastapi.templating import (
    Jinja2Templates,
)
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
)

import secrets
import requests
from utils import (
    motion_stream_iterator,
)
from core.config import (
    settings,
)

# Requried
MOTION_CAM_URL = settings.motion_camera_url
USER_NAME = settings.user_name
USER_PWD = settings.user_pwd

# Optional
CHUNK_SIZE = settings.chunk_size

SECURITY = HTTPBasic(
    realm="Please enter your username and password"
)
def verify_credentials(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(SECURITY),
    ],
) -> HTTPBasicCredentials:
    username_matches = secrets.compare_digest(
        credentials.username.encode("utf-8"),
        USER_NAME.encode("utf-8"),
    )
    pwd_matches = secrets.compare_digest(
        credentials.password.encode("utf-8"),
        USER_PWD.encode("utf-8"),
    )

    if not (username_matches and pwd_matches):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers=SECURITY.make_authenticate_headers(),
        )

    return credentials

app = FastAPI(
    title="Camera API",
    doc_url=None,
    redoc_url=None,
    openapi_url=None,
    debug=False,
)

# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# Jinja2 template directory
templates = Jinja2Templates(directory = "templates")

@app.get(
    "/motion/camera",
    response_class=StreamingResponse
)
def camera(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(verify_credentials)
    ]
) -> StreamingResponse:
    try:
        upstream = requests.get(
            MOTION_CAM_URL,
            auth = (
                credentials.username,
                credentials.password
            ),
            stream=True,
            timeout=(5, None)  # (connect timeout, read timeout)
        )
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching camera stream: {e}"
        )
    if upstream.status_code != 200:
        status_code = upstream.status_code
        upstream.close()  # Close the upstream response to free resources
        
        raise HTTPException(
            status_code=status_code,
            detail=f"Error fetching camera stream: {upstream.reason}"
        )
    
    content_type = upstream.headers.get(
        "Content-Type",
        "application/octet-stream"  # Default to binary stream if not specified
    )

    return StreamingResponse(
        motion_stream_iterator(
            upstream=upstream,
            chunk_size=CHUNK_SIZE
        ),
        media_type=content_type,
    )


# Index page
@app.get(
    "/",
    response_class=HTMLResponse
)
async def index(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(verify_credentials)
    ]
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
        }
    )

if __name__ == "__main__":
    from typing import Final
    from pathlib import Path
    import uvicorn

    file_stem = Path(__file__).stem
    serve_name: Final[str] = f"{file_stem}:app"
    PORT = settings.port

    uvicorn.run(
        serve_name,
        host="127.0.0.1",
        port = PORT,
        reload=True,
    )
