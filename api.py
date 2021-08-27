import os
import time
from typing import Optional
from fastapi import FastAPI, Request, APIRouter
from fastapi.requests import HTTPConnection, Request
from fastapi.middleware import Middleware, httpsredirect
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, RedirectResponse
from starlette.responses import StreamingResponse

from dump import main, list_apps
from models import RequestedApplication

app = FastAPI(docs_url='/')


@app.get('/list')
async def list_applications(request: Request):
    listed_applications: list
    # GET APPLICATIONS FROM FRIDA LIST APPLICATION
    # listed_applications = [list_apps()]

    # Local Stored apps
    listed_applications = [f for f in os.listdir('./ipas') if os.path.isfile(os.path.join('./ipas', f))]

    return listed_applications


def ipa_stream(ipa):
    with open(ipa, 'rb') as file:
        print(file)
        yield from file


@app.post("/application", response_class=FileResponse)
def get_user_app_name(request: Request, package: RequestedApplication):
    if os.path.isfile(f'./ipas/{package.application_package}'):
        return StreamingResponse(ipa_stream(f'./ipas/{package.application_package}'),
                                 media_type='application/octet-stream')

    # Dump Application
    ipa = main(remote='192.168.155:12487', target='app_package', output_ipa='output_name')
    return FileResponse(ipa_stream(ipa), media_type='application/octet-stream .ipa')
