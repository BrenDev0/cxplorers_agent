from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from modules.agents import agent_routes
from core.middleware.auth_middleware import auth_middleware
from core.dependencies.configure_container import configure_container
from core.dependencies.container import Container
from core.services.webSocketService import WebsocketService
from core.middleware.middleware_service import MiddlewareService



@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_container()  
    yield

app = FastAPI(lifespan=lifespan)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(auth_middleware)

app.include_router(agent_routes.router)


@app.websocket("/ws/{connection_id}")
async def websocket_endpoint(websocket: WebSocket, connection_id: str, token: str = Query(None)):   
    middleware_service: MiddlewareService = Container.resolve("middleware_service")
    try:
        payload = middleware_service.verify_token(token)
        
        print(f"WebSocket authenticated user: {payload}")
    except ValueError as e:
        print(f"WebSocket auth failed: {e}")
        return

    await websocket.accept()
    websocket_service: WebsocketService = Container.resolve("websocket_service")
    websocket_service.add_connection(connection_id, websocket)
    
    print(f'Websocket connection: {connection_id} opened.')
    try:
        while True: 
            await websocket.receive_text()

    except WebSocketDisconnect:
        websocket_service.remove_connection(connection_id)
        print(f'Websocket connection: {connection_id} closed.')