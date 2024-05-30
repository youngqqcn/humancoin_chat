import time
from fastapi import Request, status
from fastapi.responses import JSONResponse
import jwt

from .redis import create_redis_client
from .reponse import HcError, create_response

def create_jwt(user_id: str, exp: int = int(time.time()) + 24*3600):
    JWT_SECRET = "GXFC@Fansland.io@2024"
    JWT_ALGORITHM = "HS256"
    return jwt.encode(key=JWT_SECRET, algorithm=JWT_ALGORITHM, payload={
        "user_id": user_id,
        "exp": exp
    })



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
    try:
        jwt_token = request.headers.get("Human-Token")
        if jwt_token is None:
            raise Exception("missing token")

        #解析token
        json_body = await request.json()
        user_id = json_body["user_id"]
        if not verify_jwt(jwtoken=jwt_token, user_id=user_id):
            raise Exception("token verify failed")

        # 获取redis中的token
        rdc = create_redis_client(db=0)
        token  = rdc.get('authtoken:{}'.format(user_id))
        if token is None:
            raise Exception("token is not in redis")
        if str(token).strip() != jwt_token.strip():
            raise Exception("token is not matched")

        return await call_next(request)
    except Exception as e:
        print('jwt_middleware error: {}'.format(e))
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=create_response(
                code=HcError.AUTH_FAIL
            ).dict(),
        )



def main():
    print(create_jwt('123456'))
    jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTIzNDU2IiwiZXhwIjoxNzE2OTUwMTI2LCJ1c2VyX3R5cGUiOjJ9.3sgPoiOaEse2DQ2z1rxdOI_ymY8B4chjJAW4lV0j3Ik"
    if verify_jwt(jwtoken=jwt_token, user_id='123456'):
        print("ok")
    else:
        print("failed")

    pass


if __name__ == "__main__":
    main()
