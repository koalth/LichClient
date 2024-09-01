from typing import List
from pydantic import BaseModel, ConfigDict, computed_field
import statistics
import math


class Base(BaseModel):
    model_config = ConfigDict(extra="ignore")


class CharacterResponse(Base):
    name: str


class ItemLevelResponse(Base):
    value: int


class ItemSlotResponse(Base):
    type: str


class ItemResponse(Base):
    level: ItemLevelResponse
    slot: ItemSlotResponse


class CharacterEquipmentResponse(Base):
    character: CharacterResponse
    equipped_items: List[ItemResponse]

    @computed_field()
    @property
    def item_level(self) -> int:
        slots_to_not_check = set(["TABARD", "SHIRT"])
        item_levels = [
            item.level.value
            for item in self.equipped_items
            if item.slot.type not in slots_to_not_check
        ]
        return int(math.floor(statistics.fmean(item_levels)))


class CharacterGenderResponse(Base):
    name: str


class CharacterFactionResponse(Base):
    name: str


class CharacterRaceResponse(Base):
    name: str


class CharacterClassResponse(Base):
    name: str


class CharacterActiveSpecResponse(Base):
    name: str


class CharacterRealmResponse(Base):
    name: str


class CharacterGuildResponse(Base):
    name: str
    id: int


class CharacterProfileResponse(Base):
    id: int
    name: str
    level: int
    average_item_level: int
    equipped_item_level: int

    guild: CharacterGuildResponse
    realm: CharacterRealmResponse
    active_spec: CharacterActiveSpecResponse
    character_class: CharacterClassResponse
    race: CharacterRaceResponse
    faction: CharacterFactionResponse
    gender: CharacterGenderResponse
