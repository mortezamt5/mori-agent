import re
import httpx

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:4b"


async def generate_response(messages: list[dict]) -> dict:
    async with httpx.AsyncClient(timeout=300) as client:
        response = await client.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "think": True,
            },
        )

        response.raise_for_status()
        result = response.json()

        raw_content = result["message"].get("content", "")
        thinking = result["message"].get("thinking", "")

        # Extract thinking if it is embedded inside content
        match = re.search(
            r"<think>(.*?)</think>",
            raw_content,
            re.DOTALL,
        )

        if match:
            thinking = thinking or match.group(1).strip()
            raw_content = re.sub(
                r"<think>.*?</think>",
                "",
                raw_content,
                flags=re.DOTALL,
            ).strip()

        return {
            "thinking": thinking,
            "content": raw_content,
        }