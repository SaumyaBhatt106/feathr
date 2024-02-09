import os
import uvicorn
import traceback

from typing import Dict
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from .router import router
from .registry import *
from .registry.db_registry import ConflictError

# rp = "/"
# try:
#     rp = os.environ["API_BASE"]
#     if rp[0] != '/':
#         rp = '/' + rp
# except:
#     pass
# print("Using API BASE: ", rp)

def get_application() -> FastAPI:
    application = FastAPI()
    # Enables CORS
    application.add_middleware(CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                    )
    # application.include_router(prefix=rp, router=api_router)
    application.include_router(router=router)
    return application


app = get_application()

def exc_to_content(e: Exception) -> Dict:
    content={"message": str(e)}
    if os.environ.get("REGISTRY_DEBUGGING"):
        content["traceback"] = "".join(traceback.TracebackException.from_exception(e).format())
    return content

@app.exception_handler(ConflictError)
async def conflict_error_handler(_, exc: ConflictError):
    return JSONResponse(
        status_code=409,
        content=exc_to_content(exc),
    )


@app.exception_handler(ValueError)
async def value_error_handler(_, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content=exc_to_content(exc),
    )

@app.exception_handler(TypeError)
async def type_error_handler(_, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content=exc_to_content(exc),
    )


@app.exception_handler(KeyError)
async def key_error_handler(_, exc: KeyError):
    return JSONResponse(
        status_code=404,
        content=exc_to_content(exc),
    )

@app.exception_handler(IndexError)
async def index_error_handler(_, exc: IndexError):
    return JSONResponse(
        status_code=404,
        content=exc_to_content(exc),
    )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)