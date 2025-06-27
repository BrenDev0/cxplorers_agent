from modules.prompts.prompts_service import PromptsService
from langchain_openai import ChatOpenAI
from fastapi import WebSocket

class PromptedHtmlComponentEditor:
    def __init__(self, prompts_service: PromptsService):
        self.prompts_service = prompts_service


    async def interact(self, user_id: str, input: str, websocket: WebSocket):
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=1.0
        )

        prompt = await self.prompts_service.get_html_editor_prompt(user_id=user_id, input=input);

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

        