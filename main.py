#!/usr/bin/env python3
from __future__ import annotations

# from dataclasses import dataclass
import pyray as pr

# from math import floor
import numpy as np
from raylib import ffi
from typing import Any

MAX_ENTITIES: int = 1024


#### ###### ####
#### CONFIG ####
#### ###### ####

#### ########## ####
#### COMPONENTS ####
#### ########## ####

#### ####### ####
#### SYSTEMS ####
#### ####### ####


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


class Assets:
    def __init__(self):
        self.textures: list[pr.Texture] = []
        self.fonts: list[pr.Font] = []

    def load_texture(self, path: str) -> int:
        tex = pr.load_texture(path)
        self.textures.append(tex)
        return len(self.textures) - 1

    def unload(self):
        for tex in self.textures:
            pr.unload_texture(tex)


class SpriteRenderer:
    def __init__(self):
        self.origin = pr.Vector2(0, 0)
        self.src: Any = ffi.new("struct Rectangle *")[0]
        self.dest: Any = ffi.new("struct Rectangle *")[0]
        self.current_tex_id = -1
        self.tex = None

    def draw_sprite(self, world: World, assets: Assets, id: int):
        tid = world.texture_id[id]

        if tid != self.current_tex_id:
            self.tex = assets.textures[tid]
            self.current_tex_id = tid

        if not self.tex:
            return

        self.src.x = world.src_x[id]
        self.src.y = world.src_y[id]
        self.src.width = world.src_w[id]
        self.src.height = world.src_h[id]

        self.dest.x = world.position_x[id]
        self.dest.y = world.position_y[id]
        self.dest.width = world.src_w[id] * world.scale[id]
        self.dest.height = world.src_h[id] * world.scale[id]

        pr.draw_texture_pro(
            self.tex,
            self.src,
            self.dest,
            self.origin,
            world.rotation[id],
            pr.WHITE,
        )  # type: ignore


def render_system(
    world: World, assets: Assets, sprite_renderer: SpriteRenderer, camera: pr.Camera2D
):
    pr.begin_drawing()
    pr.clear_background(pr.GRAY)
    pr.begin_mode_2d(camera)

    order = np.argsort(world.texture_id[: world.count])
    for i in order:
        sprite_renderer.draw_sprite(world, assets, i)

    pr.end_mode_2d()

    pr.end_drawing()


def create_iso_grid(world: World, tex_id_ground: int, camera: pr.Camera2D):
    tile_src_w = 32

    tile_w = 256
    tile_h = tile_w // 2
    tile_w_half = tile_w // 2
    tile_h_half = tile_h // 2

    grid_resolution = 4
    grid_columns, grid_rows = grid_resolution, grid_resolution
    # grid_cell_count = grid_columns * grid_rows

    scale = tile_w / tile_src_w

    camera_tile_x_offset = -(tile_w_half)
    camera_tile_y_offset = -(tile_h_half * grid_resolution + tile_h_half)

    camera.offset.x += camera_tile_x_offset
    camera.offset.y += camera_tile_y_offset

    for y in range(grid_rows):
        for x in range(grid_columns):
            pos_x = (x - y) * tile_w_half
            pos_y = (x + y) * tile_h_half

            id = world.count
            world.count += 1

            world.texture_id[id] = tex_id_ground

            world.position_x[id] = pos_x
            world.position_y[id] = pos_y

            world.src_x[id] = 1
            world.src_y[id] = 1
            world.src_w[id] = 32
            world.src_h[id] = 32

            world.scale[id] = scale


# class IsometricGrid:
#     def __init__(self, world: World, tile_width: int, grid_resolution: int):
#         self.tile_width = tile_width
#         self.tile_height = tile_width // 2
#         self.grid_resolution = grid_resolution
#
#         self.create_grid(world)
#
#     def iso_to_screen(self, x, y):
#         tile_w = self.tile_width
#         tile_h = self.tile_height
#
#         screen_x = (x - y) * (tile_w / 2)
#         screen_y = (x + y) * (tile_h / 2)
#
#         screen_x += tile_w / 2
#         screen_y += tile_h / 2
#
#         return (screen_x, screen_y)
#
#     def create_grid(self, world: World):
#         columns = self.grid_resolution
#         rows = self.grid_resolution
#
#         tile_w = self.tile_width
#
#         tile_tex = pr.load_texture("./art/iso_tile_grass.png")
#
#         tile_source = pr.Rectangle(1, 1, 32, 32)
#         origin = pr.Vector2(tile_w / 2, tile_w / 4)


def main():
    screen_w, screen_h = (1080, 720)

    game_title = "game"
    pr.init_window(screen_w, screen_h, game_title)

    pr.set_target_fps(60)
    pr.set_exit_key(pr.KeyboardKey.KEY_Q)

    world = World()
    assets = Assets()
    sprite_renderer = SpriteRenderer()

    tex_grass_id = assets.load_texture("./art/iso_tile_grass.png")

    camera = pr.Camera2D()
    camera.zoom = 1
    camera.offset = pr.Vector2(0, 0)
    camera.rotation = 0
    camera.target = pr.Vector2(-(screen_w / 2), -(screen_h / 2))

    create_iso_grid(world, tex_grass_id, camera)

    while not pr.window_should_close():
        render_system(world, assets, sprite_renderer, camera)


if __name__ == "__main__":
    main()


# def movement_system(world: World):
#     for e in world.entities:
#         if e in world.positions and e in world.velocities:
#             pos = world.positions[e]
#             vel = world.velocities[e]
#             pos.x += vel.dx
#             pos.y += vel.dy


# def update_sprite_position(sprite: Sprite, position: Position):
#     dest = sprite.dest
#     dest.x = position.x
#     dest.y = position.y


# def draw_sprite(sprite: Sprite):
#     texture = sprite.texture
#     source = sprite.source
#     dest = sprite.dest
#     origin = sprite.origin
#     rotation = sprite.rotation
#     tint = sprite.tint

#     pr.draw_texture_pro(texture, source, dest, origin, rotation, tint)

# def render_system(world: World):
#     for e in world.entities:
#         if e in world.positions and e in world.sprites:
#             position = world.positions[e]
#             sprite = world.sprites[e]
#             # update_sprite_position(sprite, position)
#             draw_sprite(sprite)


#### ##### ####
#### WORLD ####
#### ##### ####

# COMPONENTS #

# self.iso_positions: dict[Entity, IsoPosition] = dict()

# self.debug_color: dict[Entity, pr.Color] = dict()

# def create_entity(self) -> Entity:
#     entity_id = self.next_entity_id
#     self.next_entity_id += 1
#     entity = Entity(entity_id
#     self.entities.add(entity)
#     return entity


# def debug_color(index: int, length: int):
#     t = (index / length) * 255
#
#     r = 255 - t
#     r = int(min(max(r, 0), 255))
#
#     g = t
#     g = int(min(max(g, 0), 255))
#
#     b = 0
#     a = 255
#
#     return pr.Color(r, g, b, a)


# class IsometricGrid:
#     def __init__(self, world: World, tile_width: int, grid_resolution: int):
#         self.tile_width = tile_width
#         self.tile_height = tile_width // 2
#         self.grid_resolution = grid_resolution
#
#         self.create_grid(world)
#
#     def iso_to_screen(self, x, y):
#         tile_w = self.tile_width
#         tile_h = self.tile_height
#
#         screen_x = (x - y) * (tile_w / 2)
#         screen_y = (x + y) * (tile_h / 2)
#
#         screen_x += tile_w / 2
#         screen_y += tile_h / 2
#
#         return (screen_x, screen_y)
#
#     def create_grid(self, world: World):
#         columns = self.grid_resolution
#         rows = self.grid_resolution
#
#         tile_w = self.tile_width
#
#         tile_tex = pr.load_texture("./art/iso_tile_grass.png")
#
#         tile_source = pr.Rectangle(1, 1, 32, 32)
#         origin = pr.Vector2(tile_w / 2, tile_w / 4)

# for y in range(columns):
#     for x in range(rows):
#         xx, yy = self.iso_to_screen(x, y)
#         pos = Positions(xx, yy)
#         id = world.create_entity()
#         world.positions[id] = pos
#
#         idx = y * columns + x
#         length = columns * rows
#         world.debug_color[id] = debug_color(idx, length)
#         world.iso_positions[id] = IsoPosition(x, y)
#
#         tile_dest = pr.Rectangle(0, 0, tile_w, tile_w)
#
#         world.sprites[id] = Sprite(
#             tile_tex, tile_source, tile_dest, origin, 0, pr.WHITE
#         )
#         update_sprite_position(world.sprites[id], pos)

# def draw_grid(self, world: World):
#     renderables = []
#
#     for e in world.entities:
#         if e in world.positions and e in world.iso_positions and e in world.sprites:
#             iso_pos = world.iso_positions[e]
#             gx, gy = iso_pos.grid_x, iso_pos.grid_y
#             renderables.append((gx + gy, e))
#
#     renderables.sort(key=lambda x: x[0])
#
#     for _, e in renderables:
#         draw_sprite(world.sprites[e])

# def grid_center_offset(self):
#     tile_w = self.tile_width
#     size = self.grid_resolution
#     x_offset = -(tile_w // 2)
#     y_offset = -(((tile_w // 2) * (size // 2)) + tile_w // 8)
#     return (x_offset, y_offset)

# def draw_debug_grid(self, world: World):
#     tile_w = self.tile_width
#
#     for e in world.positions:
#         pos = world.positions[e]
#         pos_x = pos.x - (tile_w / 2)
#         pos_y = pos.y - (tile_w / 4)
#
#         col = world.debug_color[e]
#         pr.draw_rectangle(
#             int(pos_x) + 4, int(pos_y) + 4, tile_w - 8, (tile_w // 2) - 4, col
#         )
#         pr.draw_rectangle_lines(
#             int(pos_x) + 2, int(pos_y) + 2, tile_w - 4, tile_w - 4, pr.BLACK
#         )

# def pick_tile(self, camera: pr.Camera2D):
#     mouse_pos = pr.get_screen_to_world_2d(pr.get_mouse_position(), camera)
#
#     tile_width = self.tile_width
#     tile_height = self.tile_height
#
#     nx = mouse_pos.x / (tile_width / 2)
#     ny = mouse_pos.y / (tile_height / 2)
#
#     gx = (nx + ny) / 2
#     gy = (ny - nx) / 2
#
#     tx = floor(gx)
#     ty = floor(gy)
#
#     cx, cy = self.iso_to_screen(tx, ty)
#
#     dx = mouse_pos.x - cx
#     dy = mouse_pos.y - cy
#
#     dx /= tile_width / 2
#     dy /= tile_height / 2
#
#     if abs(dx) + abs(dy) > 1:
#         if dx > 0 and dy > 0:
#             tx += 1
#         elif dx < 0 and dy > 0:
#             ty += 1
#         elif dx < 0 and dy < 0:
#             tx -= 1
#         elif dx > 0 and dy < 0:
#             ty -= 1
#
#     return (tx, ty)


#### ################ ####
#### MAIN_ENTRY_POINT ####
#### ################ ####
# def main():
#     render_config = RenderConfig()
#     screen_w = render_config.screen_width
#     screen_h = render_config.screen_height
#     title = render_config.game_title
#
#     pr.init_window(screen_w, screen_h, title)
#     fps = render_config.fps
#     pr.set_target_fps(fps)
#     pr.set_exit_key(pr.KeyboardKey.KEY_Q)
#
#     world = World()
#
#     iso_tile_w = 200
#     iso_grid_res = 8
#     iso_grid = IsometricGrid(world, iso_tile_w, iso_grid_res)
#
#     camera_tile_x_offset, camera_tile_y_offset = iso_grid.grid_center_offset()
#
#     camera = pr.Camera2D()
#     camera.zoom = 1
#     camera.offset = pr.Vector2(
#         (screen_w / 2) + (camera_tile_x_offset * camera.zoom),
#         (screen_h / 2) + (camera_tile_y_offset * camera.zoom),
#     )
#     camera.rotation = 0
#     camera.target = pr.Vector2(0, 0)
#
#     debug = False
#
#     while not pr.window_should_close():
#         key_pressed = pr.get_key_pressed()
#         if key_pressed == pr.KeyboardKey.KEY_I:
#             debug = not debug
#
#         pr.begin_drawing()
#         pr.clear_background(pr.GRAY)
#
#         pr.begin_mode_2d(camera)
#
#         if debug:
#             iso_grid.draw_debug_grid(world)
#
#         iso_grid.draw_grid(world)
#
#         if debug:
#             pr.draw_circle(
#                 iso_tile_w // 2,
#                 (((iso_tile_w // 8) * (iso_grid_res * 2 - 1)) + iso_tile_w // 4),
#                 (6 / camera.zoom),
#                 pr.SKYBLUE,
#             )
#
#         tile_coords = iso_grid.pick_tile(camera)
#         tx, ty = tile_coords
#
#         for e in world.entities:
#             if e in world.iso_positions and e in world.positions:
#
#                 iso_pos = world.iso_positions[e]
#                 iso_x, iso_y = iso_pos.grid_x, iso_pos.grid_y
#                 pos = world.positions[e]
#                 xx, yy = int(pos.x), int(pos.y)
#
#                 if debug:
#                     if iso_y == ty and iso_x == tx:
#                         pr.draw_circle(
#                             xx,
#                             yy,
#                             16,
#                             pr.GOLD,
#                         )
#                     elif iso_x == tx:
#                         pr.draw_circle(xx, yy, 8, pr.WHITE)
#                     elif iso_y == ty:
#                         pr.draw_circle(xx, yy, 8, pr.BLUE)
#
#         pr.end_mode_2d()
#
#         if debug:
#             pr.draw_circle(screen_w // 2, screen_h // 2, 4, pr.DARKPURPLE)
#
#         pr.end_drawing()
