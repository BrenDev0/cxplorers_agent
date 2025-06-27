from core.services.redis_service import RedisService
from langchain.schema import SystemMessage, HumanMessage, AIMessage

class PromptsService: 
    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service

    async def get_examples(self, query: str): 
        pass    

    async def get_html_generation_prompt(self, user_id: str, input: str):
        system_prompt = """
        You are an expert React developer specializing in clean, modern components styled exclusively with Tailwind CSS.

        Your task is to generate a fully functional and production-ready React component based on the user's request.

        Requirements:
        - Use React hooks (e.g., useState, useEffect, useRef) where relevant to fulfill the component's functionality.
        - Style all elements using Tailwind CSS only.
        - Ensure the component is self-contained and syntactically correct.
        - Do not include any Markdown formatting (like ```), explanations, or comments.
        - Do not include extra text or messages before or after the code.
        - Output only valid, runnable React component code.

        Do:
        - Use functional components.
        - Use clean, idiomatic TSX.
        - Add basic accessibility and responsive design when appropriate.
        - Keep the component focused on its core purpose.

        Don't:
        - Include setup code (like import React from 'react') unless required for specific hooks or libraries.
        - Output anything except the code itself.
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


