from passlib.hash import pbkdf2_sha256
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.config.setting import settings
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/images", StaticFiles(directory="uploaded/images",
          html=True), name="images")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    print("Cors settings : ", settings.BACKEND_CORS_ORIGINS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    print("No cors settings")

app.include_router(api_router, prefix="/api/v2")
