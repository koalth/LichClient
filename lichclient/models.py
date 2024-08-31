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


# class ItemNameResponse(Base):
#     en_US: str

#     @computed_field
#     def value(self) -> str:
#         return self.en_US


class ItemResponse(Base):
    level: ItemLevelResponse
    # name: ItemNameResponse

class CharacterEquipmentResponse(Base):
    character: CharacterResponse
    equipped_items: List[ItemResponse]

    @computed_field
    def item_level(self) -> int:
        item_levels = [
            item.level.value for item in self.equipped_items if item.level.value > 400
        ]
        return int(math.floor(statistics.fmean(item_levels)))
