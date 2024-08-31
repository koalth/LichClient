import os
import asyncio
import dotenv
from .client import LichClient

dotenv.load_dotenv()


async def main():

    client_id = os.getenv("WOW_CLIENT_ID")
    client_secret = os.getenv("WOW_CLIENT_SECRET")

    client = LichClient(client_id, client_secret)

    data = await client.getCharacterProfile("Turing", "Dalaran", "us")

    print(data)

    # async with BlizzardClient(client_id, client_secret) as client:
    #     response = await client.get_character_equipment("turing", "dalaran")
    #     print(response)


def run():
    asyncio.run(main())
