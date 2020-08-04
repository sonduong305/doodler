import os

import uvicorn
from api.routes.api import router as api_router
from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from core.events import create_start_app_handler
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from services.mobilenet import model


parent_dir_path = os.path.dirname(os.path.realpath(__file__))


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.include_router(api_router, prefix=API_PREFIX)
    pre_load = False
    model.load_model()
    model.warm_up()
    print('model loaded')
    if pre_load:
        application.add_event_handler(
            "startup", create_start_app_handler(application))
    return application


app = get_application()
app.mount("/statics", StaticFiles(directory="app/statics"), name="statics")


@app.get("/")
async def redirect():
    response = RedirectResponse(url='/statics/index.html')
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=8080, reload=DEBUG, debug=DEBUG)
