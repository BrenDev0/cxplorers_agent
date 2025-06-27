from modules.prompts.prompts_service import PromptsService
from langchain_openai import ChatOpenAI
from fastapi import WebSocket
from core.dependencies.container import Container
from core.services.s3_service import S3Service
import subprocess

class PromptedHtmlComponentGenerator:
    def __init__(self, prompts_service: PromptsService):
        self.prompts_service = prompts_service


    async def generate_react_component(self, user_id: str, input: str, websocket: WebSocket):
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=1.0
        )

        prompt = await self.prompts_service.get_html_generation_prompt(user_id=user_id, input=input);


        # try: 
            # response = await llm.ainvoke(prompt)

            # code = self.transpile_jsx_with_babel(response.content)
            # s3_service: S3Service = Container.resolve("s3_service")
            # url = s3_service.upload(
            #     user_id=user_id,
            #     foldername="agent-genrated/components",
            #     file_content=code,
            #     content_type="application/javascript"
            # )

            # print(url)

            # return response.content
        # except Exception as e: 
        #     print(e)
        try:
            async for chunck in llm.astream(prompt):
                if hasattr(chunck, "content") and chunck.content:
                    await websocket.send_text(chunck.content)
        except RuntimeError as ws_err:
            print(f"websocket connection already closed: {ws_err}")
        except Exception as e:
            print(f"Unexpected WebSocket error: {e}")

        
        try:
            await websocket.send_json({ "closeConnection": True })
        except: 
            pass


