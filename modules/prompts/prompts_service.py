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

        Your task is to generate a **complete React component file** written in **javascript** (not TypeScript). Use **Tailwind CSS** exclusively for styling, and include **JSDoc annotations** for the component and all props.

        ## Output Requirements:
        - Output only valid, raw javascript code as it would appear in a `.js` file.
        - Do **not** include Markdown formatting, backticks, or code fences.
        - Do **not** add any extra text or explanations (e.g., "Here is your component").
        - Do **not** wrap the code in quotes.
        - The output must be **copy-pasteable directly** into a `.jsx` file with **no cleanup required**.
        - Include:
        - JSDoc block above the component definition.
        - JSDoc block above each prop explaining its type and usage.

        ## Component Requirements:
        - Use functional components and Hooks (if needed).
        - Style everything with **Tailwind CSS only** — no inline styles or external stylesheets.
        - Ensure the component is clean, readable, and idiomatic React.

        ## Example request:
        "A card component that displays a title and description, with a button to expand more text."


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


