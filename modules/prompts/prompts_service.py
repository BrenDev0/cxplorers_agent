from core.services.redis_service import RedisService
from langchain.schema import SystemMessage, HumanMessage, AIMessage

class PromptsService: 
    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service

    async def get_examples(self, query: str): 
        pass    

    async def get_html_generation_prompt(self, user_id: str, input: str):
        system_prompt = """
        You are an expert React developer.

        Your task is to generate a complete React component file in JavaScript (not TypeScript), styled with Tailwind CSS, and including proper JSDoc annotations.

        Output Rules:
        - Do NOT wrap the code in Markdown, backticks, or any kind of formatting.
        - Do NOT include comments like "Here is your component" or "```js".
        - Only return raw JavaScript code — as it would appear in a real .js file.
        - DO include JSDoc above the component definition and above each prop.
        - Use Tailwind CSS exclusively for all styling.

        The final output should be copy-pasteable directly as a .js file without cleanup.

        Example request: "A card component that displays a title and description, with a button to expand more text."

        """
        messages = [SystemMessage(content=system_prompt.strip())]

        chat_history = await self.redis_service.get_session(f"html_generation_history:{user_id}")
        
        if chat_history:
            for msg in chat_history:
                if msg["sender"] == "client":
                    messages.append(HumanMessage(content=msg["text"]))
                elif msg["sender"] == "agent":
                    messages.append(AIMessage(content=msg["text"]))

        messages.append(HumanMessage(content=input.strip()))
    
        return messages


    async def get_html_editor_prompt(self, user_id: str, input: str): 
        system_prompt ="""
            You are an expert in generating HTML andTailwind css.
            
            Your task is to edit HTML components according the the clients input.

            - IMPORTANT - Do not include any explanations, Markdown formatting (like ```), or extra text.
            - IMPORTANT - Do not incluede any HTML boilerplate (no <html>, <head>, <body>, or <script> tags)
            - IMPORTANT - Only return raw HTML.

            Your output must:
            - Be valid HTML
            - Use only valid Tailwind CSS classes
            """
        messages = [
            SystemMessage(content=system_prompt)
        ]

        chat_history = await self.redis_service.get_session(f"html_generation_history:{user_id}")
        
        if chat_history:
            for msg in chat_history:
                if msg["sender"] == "client":
                    messages.append(HumanMessage(content=msg["text"]))
                elif msg["sender"] == "agent":
                    messages.append(AIMessage(content=msg["text"]))

        messages.append(HumanMessage(content=input.strip()))
    
        return messages


