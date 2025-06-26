from modules.prompts.prompts_service import PromptsService
from langchain_openai import ChatOpenAI

class PromptedHtmlComponentEditor:
    def __init__(self, prompts_service: PromptsService):
        self.prompts_service = prompts_service


    async def interact(self, user_id: str, input: str):
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=1.0
        )

        prompt = await self.prompts_service.get_html_editor_prompt(user_id=user_id, input=input);

        response = await llm.ainvoke(prompt)

        return response.content

        