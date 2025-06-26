from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request, HTTPException
from fastapi.responses import JSONResponse
from core.dependencies.container import Container
from modules.agents.prompted_html_generator import PromptedHtmlComponentGenerator
from modules.agents.propted_html_editor import PromptedHtmlComponentEditor
from modules.agents.agent_models import HtmlRequest
from core.services.webSocketService import WebsocketService

router = APIRouter(
    prefix="/api/agents/html",
    tags=["Agent"]
)

@router.post("/generate", response_class=JSONResponse)
async def interact(
    request: Request,
    backgroundTasks: BackgroundTasks,
    data: HtmlRequest = Body(...),
):
    user_id = request.state.user_id
    
    websocket_service: WebsocketService = Container.resolve("websocket_service")
    websocket = websocket_service.get_connection(data.connection_id)

    if websocket is None:
        raise HTTPException(status_code=404, detail="Websocket connection not found.")
    
    prompted_html_generator: PromptedHtmlComponentGenerator = Container.resolve("prompted_html_generator")

    backgroundTasks.add_task(prompted_html_generator.interact, user_id, data.input, websocket)
    
    return JSONResponse(status_code=200, content={"message": "Request received"});


@router.post("/edit", response_class=JSONResponse)
async def interact(
    request: Request,
    backgroundTasks: BackgroundTasks,
    data: HtmlRequest = Body(...),
):
    user_id = request.state.user_id

    websocket_service: WebsocketService = Container.resolve("websocket_service")
    websocket = websocket_service.get_connection(data.connection_id)

    if websocket is None:
        raise HTTPException(status_code=404, detail="Websocket connection not found.")
    
    prompted_html_editor: PromptedHtmlComponentEditor = Container.resolve("prompted_html_generator")

    backgroundTasks.add_task(prompted_html_editor.interact, user_id, data.input, websocket)
    
    
    return JSONResponse(status_code=200, content={"message": "Request received"});