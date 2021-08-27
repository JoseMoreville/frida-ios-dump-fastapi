from pydantic import BaseModel


class RequestedApplication(BaseModel):
    application_package: str
    pass

