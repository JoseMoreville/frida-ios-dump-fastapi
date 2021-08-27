import os
import time
from typing import Optional
from fastapi import FastAPI, Request, APIRouter
from fastapi.requests import HTTPConnection, Request
from fastapi.middleware import Middleware, httpsredirect
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, RedirectResponse
from starlette.responses import StreamingResponse

from dump import remote_iphone, usb_iphone, list_apps, list_apps_usb
from models import RequestedApplication

app = FastAPI(docs_url='/')


@app.get('/list')
async def list_applications(request: Request):
    listed_applications: list
    # GET APPLICATIONS FROM FRIDA LIST APPLICATION
    try:
        listed_applications = [list_apps()]
    except:
        try:
            listed_applications = [list_apps_usb()]
        except:
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

    # Dump Application from iphone
    try:
        ipa = remote_iphone(remote='192.168.155:12487', target=package.application_package,
                            output_ipa=package.application_package)
    except:
        ipa = usb_iphone(target=package.application_package, output_ipa=package.application_package)
    return StreamingResponse(ipa_stream(package.application_package),
                             media_type='application/octet-stream')
