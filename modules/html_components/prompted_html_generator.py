from modules.prompts.prompts_service import PromptsService
from langchain_openai import ChatOpenAI
from fastapi import WebSocket
from core.dependencies.container import Container
from core.services.s3_service import S3Service

class PromptedHtmlComponentGenerator:
    def __init__(self, prompts_service: PromptsService):
        self.prompts_service = prompts_service


    async def generate_react_component(self, user_id: str, input: str, websocket: WebSocket):
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=1.0
        )

        prompt = await self.prompts_service.get_html_generation_prompt(user_id=user_id, input=input);


        full_response = ""

        try:
            async for chunk in llm.astream(prompt):
                if hasattr(chunk, "content") and chunk.content:
                    full_response += chunk.content
                    await websocket.send_text(chunk.content)

            s3_service: S3Service = Container.resolve("s3_service")
            url = s3_service.upload(
                user_id=user_id,
                foldername="agent-generated/components",
                file_content=full_response,
                content_type="application/javascript"
            )

            await websocket.send_json({ "status": "Complete", "url": url })

        except RuntimeError as ws_err:
            print(f"WebSocket closed prematurely: {ws_err}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            try:
                await websocket.send_json({"status": "error", "message": str(e)})
            except:
                pass

        finally:
            try:
                await websocket.send_json({ "closeConnection": True })
            except:
                pass