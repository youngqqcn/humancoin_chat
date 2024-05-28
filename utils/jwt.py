import jwt

JWT_SECRET = 'GXFC@Fansland.io@2024'
JWT_ALGORITHM = 'HS256'


def verify_jwt(jwtoken: str, user_id: str) -> bool:
    try:
        claims = jwt.decode(jwtoken, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(claims)
        return claims['user_id'] == user_id
    except Exception as e:
        print('error: {}'.format(e))
        return False




def main():
    # const JWT_TOKEN: &str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2FkZHJlc3MiOiIweGNkOWNmZjZhOTVkNmJiN2Q4YjhiNTBlYzg5NjUxM2U5YTJjZjY1NGEiLCJleHAiOjE3MDYwODYwNzh9.kLS1tb6wz7maiF7UgFFhlArtIu0zALqroTiUYwHFFzc";

    jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTIzNDU2IiwiZXhwIjoxNzE2OTUwMTI2LCJ1c2VyX3R5cGUiOjJ9.3sgPoiOaEse2DQ2z1rxdOI_ymY8B4chjJAW4lV0j3Ik"

    if verify_jwt(jwtoken=jwt_token):
        print('ok')
    else:
        print('failed')


    pass

if __name__ == '__main__':
    main()

