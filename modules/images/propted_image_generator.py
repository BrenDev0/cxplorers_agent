import httpx
import os

class PromptedImageGenerator:
    async def interact(self, user_id: str, input: str):
        url = "https://api.openai.com/v1/images/generations"
        headers = {"Authorization": f"Bearer {os.getenv("OPENAI_API_KEY")}"}
        data = {
            "model": "dall-e-3",
            "prompt": input,
            "n": 1,
            "size": "1024x1024"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, data=data)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            print(f"Agent handoff failed: {exc.response.status_code} - {exc.response.text}")
            return {"error": exc.response.text, "status_code": exc.response.status_code}
        
       

        