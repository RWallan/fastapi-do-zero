import jwt

from fastapi_do_zero.security import JWT


def test_jwt():
    data = {"teste": "teste"}
    token = JWT.encode(data)

    decoded = jwt.decode(token, JWT.SECRET_KEY, algorithms=[JWT.ALGORITHM])

    assert decoded["teste"] == data["teste"]
    assert decoded["exp"]
