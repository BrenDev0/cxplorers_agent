from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request, HTTPException
from fastapi.responses import JSONResponse
from core.dependencies.container import Container
from modules.agents.prompted_html_generator import PromptedHtmlComponentGenerator
from modules.agents.propted_html_editor import PromptedHtmlComponentEditor
from modules.agents.propted_image_generator import PromptedImageGenerator
from modules.agents.agent_models import HtmlRequest
from modules.agents.agent_models import ImageGenerationREquest
from core.services.webSocketService import WebsocketService


router = APIRouter(
    prefix="/api/agents",
    tags=["Agent"]
)

@router.post("/html/generate", response_class=JSONResponse)
async def generate_html_component(
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


@router.post("/html/edit", response_class=JSONResponse)
async def edit_html_component(
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

@router.post("/images/generate", response_class=JSONResponse)
async def generate_image(
        request: Request,
        data: ImageGenerationREquest = Body(...)
): 
    user_id = request.state.user_id

    prompted_image_generator: PromptedImageGenerator = Container.resolve("prompted_image_generator")
    response = await prompted_image_generator.interact(user_id=user_id, input=data.input)
    print(f"response: {response}::::::::::::::")

    return JSONResponse(status_code=200, content={"message": response});