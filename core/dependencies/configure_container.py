from sqlalchemy.orm import Session
from core.services.redis_service import RedisService
from core.dependencies.container import Container
from core.middleware.middleware_service import MiddlewareService
from core.services.webtoken_service import WebTokenService
from core.services.webSocketService import WebsocketService
from modules.prompts.prompts_service import PromptsService
from modules.agents.prompted_html_generator import PromptedHtmlComponentGenerator

def configure_container():
    # core   
    
    # Redis
    redis_service = RedisService()
    Container.register("redis_service", redis_service)

    # Webtokens
    webtoken_service = WebTokenService()
    Container.register("webtoken_service", webtoken_service)

    # Middleware
    middleware_service = MiddlewareService(
        webtoken_service=webtoken_service
    )
    Container.register("middleware_service", middleware_service)

    # Prompts
    prompts_service = PromptsService(redis_service=redis_service)
    Container.register("prompts_service", prompts_service)

    # HTML generation
    prompted_html_generator = PromptedHtmlComponentGenerator(
        prompts_service=prompts_service
    )
    Container.register("prompted_html_generator", prompted_html_generator)

    websocket_service = WebsocketService()
    Container.register("websocket_service", websocket_service)





    




