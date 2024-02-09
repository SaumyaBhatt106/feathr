import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .api import router as api_router

# rp = "/"
# try:
#     rp = config.RBAC_API_BASE
#     if rp[0] != '/':
#         rp = '/' + rp
# except:
#     pass

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
    application.include_router(router=api_router)
    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
