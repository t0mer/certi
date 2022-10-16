from fastapi import FastAPI, Request, File, Form, UploadFile, HTTPException
from fastapi.responses import UJSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse
from starlette.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from loguru import logger
import uvicorn
class Server:
    def __init__(self, db):
        self.db = db

        self.tags_metadata = [
            {
                "name": "Domains",
                "description": "Add, Remove, Update domain to monitored domains list",
            },
            {
                "name": "Certificates",
                "description": "View list of monitored or issued certificates",
            },
        ]

        self.app = FastAPI(title="Certi", description="Monitor your SSL Certificates and get notification upon new cert issue", version='1.0.0', openapi_tags=self.tags_metadata, contact={"name": "Tomer Klein", "email": "tomer.klein@gmail.com", "url": "https://github.com/t0mer/certi"})

        @self.app.get("/domains/get",tags=['Domains'], summary="Get list of monitored domains")
        def get_monitored_domains(request: Request):
            try:
                return JSONResponse(self.db.get_monitored_domains(True))
            except Exception as e:
                logger.error("Error fetch images, " + str(e))
                return None


        @self.app.put('/domains/add/{DomainName}',tags=['Domains'], summary="Add domain to monitored domains list")
        def add_domain(DomainName: str):
            try:
                result, message = self.db.add_monitored_domain(DomainName)
                return JSONResponse(content = '{"message":"'+ message +'","success":"'+ str(result).lower() +'"}')
            except Exception as e:
                logger.error(str(e))
                return JSONResponse(content = '{"message":"'+str(e)+'","success":"false"}')

        @self.app.delete('/domains/delete/{DomainId}',tags=['Domains'], summary="Remove domain from monitored domains list")
        def delete_domain(DomainId: int):
            try:
                result, message = self.db.delete_monitored_domain(DomainId)
                return JSONResponse(content = '{"message":"'+ message +'","success":"'+ str(result).lower() +'"}')
            except Exception as e:
                logger.error(str(e))
                return JSONResponse(content = '{"message":"'+str(e)+'","success":"false"}')
        
        @self.app.get("/certificates/get",tags=['Certificates'], summary="Get list of all existing certificates")
        def get_certificates(request: Request):
            try:
                return JSONResponse(self.db.get_certificates())
            except Exception as e:
                logger.error("Error fetch certificates, " + str(e))
                return None

    def start(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8081)