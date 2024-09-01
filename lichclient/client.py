from typing import List, Optional
from .blizzard import BlizzardClient
from .models import CharacterProfileResponse

from abc import ABC, abstractmethod


class ILichClient(ABC):

    @abstractmethod
    async def getCharacterProfile(
        self, name: str, realm: str, region: str
    ) -> CharacterProfileResponse:
        raise NotImplementedError()


class LichClient(ILichClient):

    client_id: str
    client_secret: str

    def __init__(self, client_id: Optional[str], client_secret: Optional[str]):
        if client_id is None:
            raise Exception("Client ID is None")

        if client_secret is None:
            raise Exception("Client Secret is None")

        self.client_id = client_id
        self.client_secret = client_secret

    async def getCharacterProfile(
        self, name: str, realm: str, region: str
    ) -> CharacterProfileResponse:
        async with BlizzardClient(self.client_id, self.client_secret) as client:
            response = await client.get_character_profile(name, realm, region="us")
            return CharacterProfileResponse(
                name=response.name,
                realm=response.realm.name,
                region=region,
                item_level=response.average_item_level,
                class_name=response.character_class.name,
                active_spec=response.active_spec.name,
                faction=response.faction.name,
                race=response.race.name,
                gender=response.gender.name,
            )
