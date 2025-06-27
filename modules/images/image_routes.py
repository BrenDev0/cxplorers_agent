from fastapi import APIRouter, Depends, Body, Request
from fastapi.responses import JSONResponse
from core.dependencies.container import Container
from modules.images.propted_image_generator import PromptedImageGenerator
from modules.images.images_models import ImageGenerationREquest


router = APIRouter(
    prefix="/api/images",
    tags=["Images"]
)



@router.post("/generate", response_class=JSONResponse)
async def generate_image(
        request: Request,
        data: ImageGenerationREquest = Body(...)
): 
    user_id = request.state.user_id

    prompted_image_generator: PromptedImageGenerator = Container.resolve("prompted_image_generator")
    response = await prompted_image_generator.interact(user_id=user_id, input=data.input)
    print(f"response: {response}::::::::::::::")

    return JSONResponse(status_code=200, content={"message": response});