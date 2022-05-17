from fastapi import APIRouter

hello_world_router = APIRouter()


@hello_world_router.get('/')
def hello_world():
    return {'message': 'Hello World'}
