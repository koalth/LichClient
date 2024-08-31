import os
import asyncio
import dotenv
import httpx
from authlib.integrations.httpx_client import AsyncOAuth2Client, OAuth2Auth
import json
from .models import CharacterEquipmentResponse

dotenv.load_dotenv()


async def main():

    auth_url = "https://oauth.battle.net/token"

    client_id = os.getenv("WOW_CLIENT_ID")
    client_secret = os.getenv("WOW_CLIENT_SECRET")

    client = AsyncOAuth2Client(client_id, client_secret)

    access_token = await client.fetch_token(auth_url)  # type: ignore
    auth = OAuth2Auth(token=access_token)

    api_url = "https://us.api.blizzard.com/profile/wow/character/dalaran/turing/equipment?namespace=profile-us"

    with httpx.Client(auth=auth) as client:
        response = client.get(api_url)
        json_data = json.dumps(response.json())
        data = CharacterEquipmentResponse.model_validate_json(json_data)
        print(data)


def run():
    asyncio.run(main())
    # main()
