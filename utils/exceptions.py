from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from utils.reponse import ResponseModel

async def http_exception_handler(request: Request, exc: HTTPException):
    print("xxxxxxxxxxxxxxxxxxxx: {}".format(exc))
    response = ResponseModel(
        code=exc.status_code,
        msg=exc.detail,
        data=None
    )
    return JSONResponse(status_code=exc.status_code, content=response.dict())

async def general_exception_handler(request: Request, exc: Exception):
    print("==============================")
    response = ResponseModel(
        code=1099,
        msg="some error occured, please try again later",
        data=None
    )

    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content=response.dict())