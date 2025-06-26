from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request
from fastapi.responses import JSONResponse
from core.dependencies.container import Container
from modules.agents.prompted_html_generator import PromptedHtmlComponentGenerator
from modules.agents.propted_html_editor import PromptedHtmlComponentEditor
from modules.agents.agent_models import GenerateHtmlRequest

router = APIRouter(
    prefix="/api/agents/html",
    tags=["Agent"]
)

@router.post("/generate", response_class=JSONResponse)
async def interact(
    request: Request,
    backgroundTasks: BackgroundTasks,
    data: GenerateHtmlRequest = Body(...),
):
    user_id = request.state.user_id
    prompted_html_generator: PromptedHtmlComponentGenerator = Container.resolve("prompted_html_generator")

    response = await prompted_html_generator.interact(user_id=user_id, input=data.input)
    
    
    return JSONResponse(status_code=200, content={"message": response});

@router.post("/edit", response_class=JSONResponse)
async def interact(
    request: Request,
    backgroundTasks: BackgroundTasks,
    data: GenerateHtmlRequest = Body(...),
):
    user_id = request.state.user_id
    prompted_html_editor: PromptedHtmlComponentEditor = Container.resolve("prompted_html_generator")

    response = await prompted_html_editor.interact(user_id=user_id, input=data.input)
    
    
    return JSONResponse(status_code=200, content={"message": response});