import asyncio
from g4f.client import AsyncClient


async def main():
    client = AsyncClient()

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": "Кто ты?"
            }
        ],
        stream=True,
    )

    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")


asyncio.run(main())