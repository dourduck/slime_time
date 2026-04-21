from __future__ import annotations
import numpy as np
from enum import IntFlag
from dataclasses import dataclass

MAX_ENTITIES = 1024


class EntityKind(IntFlag):
    NONE = 0
    PLAYER = 1 << 0
    ENEMY = 1 << 1
    TILE = 1 << 2


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

    def set_kind(self, kind: EntityKind):
        if kind & EntityKind.PLAYER:
            self.world.entity_tag_player.add(self.id)
        if kind & EntityKind.ENEMY:
            self.world.entity_tag_enemy.add(self.id)
        if kind & EntityKind.TILE:
            self.world.entity_tag_tile.add(self.id)


class World:
    def __init__(self):
        self.entities: dict[int, Entity] = dict()
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

        self.entity_tag_enemy: set[int] = set()
        self.entity_tag_tile: set[int] = set()
        self.entity_tag_player: set[int] = set()

    def create_entity(self, kind: EntityKind) -> Entity:
        id = self.count

        self.count += 1

        if self.count == MAX_ENTITIES:
            print("REACHED ENTITY MAXIMUM!!!")

        entity = Entity(id, self)
        entity.set_kind(kind)
        self.entities[id] = entity

        return entity

    def create_tile_entity(self) -> Entity:
        entity = self.create_entity(EntityKind.TILE)
        return entity
