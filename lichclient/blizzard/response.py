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
