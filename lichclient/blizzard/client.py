from authlib.integrations.httpx_client import AsyncOAuth2Client, OAuth2Auth
import httpx
from .response import CharacterEquipmentResponse, Base
import json
from typing import TypeVar, Type, Optional

ModelT = TypeVar("ModelT", bound=Base)


class BlizzardClient:

    api_url: str = "https://us.api.blizzard.com"
    auth_url: str = "https://oauth.battle.net/token"

    auth_client: AsyncOAuth2Client
    auth: Optional[OAuth2Auth]

    client: Optional[httpx.AsyncClient]

    def __init__(self, client_id: Optional[str], client_secret: Optional[str]) -> None:
        if client_id is None:
            raise Exception("Client ID is None")

        if client_secret is None:
            raise Exception("Client Secret is None")

        self.client_id = client_id
        self.client_secret = client_secret

        self.client = None
        self.access_token = None
        self.auth = None

    async def __aenter__(self):
        await self.authenticate()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        if self.client is None:
            raise Exception("Client is not initilized")

        await self.client.aclose()

    async def authenticate(self):
        async with AsyncOAuth2Client(
            client_id=self.client_id, client_secret=self.client_secret
        ) as oauth:
            access_token = await oauth.fetch_token(self.auth_url)  # type: ignore
            self.auth = OAuth2Auth(token=access_token)

        self.client = httpx.AsyncClient(base_url=self.api_url, auth=self.auth)

    async def _get(self, endpoint: str, data_cls: Type[ModelT]) -> ModelT:
        if self.client is None:
            raise Exception("Client is not initalized")
        response = await self.client.get(endpoint)
        if not response.is_success:
            raise Exception(f"Response did not succeed: {response.text}")

        json_data = json.dumps(response.json())
        return data_cls.model_validate_json(json_data)

    async def get_character_equipment(
        self, name: str, realm: str
    ) -> CharacterEquipmentResponse:
        endpoint = f"/profile/wow/character/{realm.lower()}/{name.lower()}/equipment?namespace=profile-us"
        return await self._get(endpoint, CharacterEquipmentResponse)
