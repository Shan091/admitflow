"""Async OpenAI adapter for intent decisions and embeddings."""

from openai import AsyncOpenAI


class OpenAIAdapter:
    def __init__(self, api_key: str, decisions_model: str, embedding_model: str) -> None:
        self.client = AsyncOpenAI(api_key=api_key)
        self.decisions_model = decisions_model
        self.embedding_model = embedding_model
        self.total_embedding_prompt_tokens = 0

    async def route(self, text: str) -> str:
        response = await self.client.decisions.create(
            model=self.decisions_model,
            input=text,
            questions=[
                {
                    "type": "choice",
                    "name": "intent",
                    "instructions": "Classify the student's message by its immediate intent.",
                    "choices": [
                        {"value": "knowledge_question", "description": "Asks an institution FAQ."},
                        {"value": "course_browse", "description": "Wants course information."},
                        {"value": "human_request", "description": "Explicitly asks for staff."},
                        {"value": "other", "description": "Anything else or uncertain."},
                    ],
                }
            ],
        )
        answer = response.answers[0]
        if answer.type != "choice":
            return "other"
        return str(answer.choice)

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = await self.client.embeddings.create(
            model=self.embedding_model,
            input=texts,
            encoding_format="float",
        )
        self.total_embedding_prompt_tokens += response.usage.prompt_tokens
        return [item.embedding for item in response.data]

    async def close(self) -> None:
        await self.client.close()
