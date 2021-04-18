from passlib.hash import pbkdf2_sha256

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.config.setting import settings
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/images", StaticFiles(directory="uploaded/images",
          html=True), name="images")

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

app.include_router(api_router)
