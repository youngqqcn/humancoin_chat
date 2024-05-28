from fastapi import Request, status
from fastapi.responses import JSONResponse
import jwt

from utils.utils import create_response


def verify_jwt(jwtoken: str, user_id: str) -> bool:
    JWT_SECRET = "GXFC@Fansland.io@2024"
    JWT_ALGORITHM = "HS256"

    try:
        claims = jwt.decode(jwtoken, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(claims)
        return claims["user_id"] == user_id
    except Exception as e:
        print("error: {}".format(e))
        return False


async def jwt_middleware(request: Request, call_next):
    jwt_token = request.headers.get("Human-Token")
    json_body = await request.json()
    user_id = json_body["user_id"]
    if verify_jwt(jwtoken=jwt_token, user_id=user_id):
        return await call_next(request)

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=create_response(
            msg="invalid token", code=status.HTTP_401_UNAUTHORIZED
        ).dict(),
    )


def main():
    jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTIzNDU2IiwiZXhwIjoxNzE2OTUwMTI2LCJ1c2VyX3R5cGUiOjJ9.3sgPoiOaEse2DQ2z1rxdOI_ymY8B4chjJAW4lV0j3Ik"
    if verify_jwt(jwtoken=jwt_token):
        print("ok")
    else:
        print("failed")

    pass


if __name__ == "__main__":
    main()
