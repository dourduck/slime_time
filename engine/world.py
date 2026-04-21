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


class World:
    def __init__(self):
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

        self.enemy_bucket = set()
        self.tile_bucket = set()
        self.player_bucket = set()

    def create_entity(self, kind: EntityKind) -> Entity:
        id = self.count

        self.count += 1

        if self.count == MAX_ENTITIES:
            print("REACHED ENTITY MAXIMUM!!!")

        if kind & EntityKind.PLAYER:
            # of player kind
            self.player_bucket.add(id)
        elif kind & EntityKind.ENEMY:
            # of enemy kind
            self.enemy_bucket.add(id)
        elif kind & EntityKind.TILE:
            # of tile kind
            self.tile_bucket.add(id)

        return Entity(id, self)

    def create_tile_entity(self) -> Entity:
        entity = self.create_entity(EntityKind.TILE)
        return entity
