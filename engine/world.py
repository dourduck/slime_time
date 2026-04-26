from __future__ import annotations
import numpy as np
from enum import Flag, auto
from dataclasses import dataclass

MAX_ENTITIES = 4096


class Tags(Flag):
    PLAYER = auto()  # 1
    ENEMY = auto()  # 2
    UNDEAD = auto()  # 4  # just as an example
    TILE = auto()  # 8


# Returns a masked result from the given ndarray. #
def has_flags(arr: np.ndarray, flags: Tags) -> np.ndarray:
    v = flags.value
    return (arr & v) == v


@dataclass(frozen=True)
class Entity:
    id: int
    world: World

    def add_position(self, pos_x: int, pos_y: int):
        self.world.position_x[self.id] = pos_x
        self.world.position_y[self.id] = pos_y

    def add_scale(self, scale: float):
        self.world.scale[self.id] = scale

    def add_texture(self, texture_id: int):
        self.world.texture_id[self.id] = texture_id

    def add_texture_src_rect(self, x: int, y: int, w: int, h: int):
        self.world.src_x[self.id] = x
        self.world.src_y[self.id] = y
        self.world.src_w[self.id] = w
        self.world.src_h[self.id] = h

    def set_tags(self, tags: Tags):
        self.world.entity_tags[self.id] = tags.value


class World:
    def __init__(self):
        # self.entities: dict[int, Entity] = dict()
        self.position_x = np.zeros(MAX_ENTITIES, dtype=np.float32)
        self.position_y = np.zeros(MAX_ENTITIES, dtype=np.float32)
        self.velocity_x = np.zeros(MAX_ENTITIES, dtype=np.float32)
        self.velocity_y = np.zeros(MAX_ENTITIES, dtype=np.float32)

        self.texture_id = np.zeros(MAX_ENTITIES, dtype=np.int32)
        self.src_x = np.zeros(MAX_ENTITIES, dtype=np.float32)
        self.src_y = np.zeros(MAX_ENTITIES, dtype=np.float32)
        self.src_w = np.zeros(MAX_ENTITIES, dtype=np.float32)
        self.src_h = np.zeros(MAX_ENTITIES, dtype=np.float32)
        self.scale = np.ones(MAX_ENTITIES, dtype=np.float32)
        self.rotation = np.zeros(MAX_ENTITIES, dtype=np.float32)

        self.count = 0

        self.entity_tags = np.zeros(MAX_ENTITIES, dtype=np.uint8)

    def create_entity(self, tags: Tags) -> Entity:
        id = self.count

        self.count += 1

        if self.count == MAX_ENTITIES:
            print("REACHED ENTITY MAXIMUM!!!")

        entity = Entity(id, self)
        entity.set_tags(tags)
        # self.entities[id] = entity

        return entity

    def create_tile_entity(self) -> Entity:
        entity = self.create_entity(Tags.TILE)
        return entity
