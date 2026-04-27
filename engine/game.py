from dataclasses import dataclass
import global_state as glb
import pyray as pr
import asset

# import numpy as np

# import world as wor


# class TileData:
#     grid_x: np.ndarray
#     grid_y: np.ndarray
#
#     @staticmethod
#     def tile_indices_draw_order(columns: int, rows: int):
#         X, Y = np.meshgrid(np.arange(columns), np.arange(rows))
#         depth = (X + Y).reshape(-1)
#         indices = np.argsort(depth)
#         return indices


class Game:
    def __init__(self, global_state: glb.GlobalState):
        self.world = global_state.world
        self.input_state = global_state.input_state
        self.renderer = global_state.renderer

    def loop(self):
        renderer = self.renderer
        input_state = self.input_state
        world = self.world

        renderer.create_raylib_window()

        #### RENDER TEST
        assets = asset.Assets()
        path_tile_grass = assets.get_path(asset.AssetID.TEX_TILE_GRASS)
        tile_tex_grass_id = renderer.load_texture(path_tile_grass)

        #### END RENDER TEST

        #### ISO GRID
        desired_tile_w = 180
        tile_src_w = 32
        tile_src_h = 32
        tile_src_x = 1
        tile_src_y = 1
        tile_scale = desired_tile_w / tile_src_w
        grid_resolution = 10
        grid_resolution_half = grid_resolution // 2

        for y in range(-grid_resolution_half, grid_resolution_half):
            for x in range(-grid_resolution_half, grid_resolution_half):
                tile_entity = world.create_tile_entity()
                pos_x = int((x - y) * (tile_src_w * tile_scale) / 2)
                pos_y = int((x + y) * (tile_src_h * tile_scale) / 4)
                pos_x -= int((tile_src_w * tile_scale) / 2)
                pos_y -= int((tile_src_h * tile_scale) / 4)

                tile_entity.add_texture(tile_tex_grass_id)
                tile_entity.add_position(pos_x, pos_y)
                tile_entity.add_scale(tile_scale)
                tile_entity.add_texture_src_rect(
                    tile_src_x, tile_src_y, tile_src_w, tile_src_h
                )

        ####

        #### data mutation via tag test
        # entity_tile_mask = wor.has_flags(world.entity_tags, wor.Tags.TILE)
        # entity_tile_ids = np.flatnonzero(entity_tile_mask)
        # if len(entity_tile_ids):
        #     world.entity_tags[entity_tile_ids[0]] |= wor.Tags.ENEMY.value
        #
        #     entity_tile_enemy_mask = wor.has_flags(
        #         world.entity_tags, (wor.Tags.TILE | wor.Tags.ENEMY)
        #     )
        #     entity_tile_enemy_ids = np.flatnonzero(entity_tile_enemy_mask)
        #
        #     for eid in entity_tile_ids:
        #         print(f"tile entity id: {eid}")
        #     for eid in entity_tile_enemy_ids:
        #         print(f"tile+enemy entity id: {eid}")
        #         world.position_x[eid] -= 400
        #         world.position_y[eid] -= 200
        ####

        #### SLIME ANIM ####
        path_anim_slime = assets.get_path(asset.AssetID.TEX_ANIM_SLIME)

        # slime_anim_id = renderer.load_texture(path_anim_slime)  # (16 x 16) 4 frames
        slime_anim = pr.load_texture(path_anim_slime)

        slime_frames = list()
        frame_width = 16
        frame_height = 16
        for i in range(4):
            frame_scr = pr.Rectangle(
                i * frame_width, frame_height, frame_width, frame_height
            )
            slime_frames.append(frame_scr)

        slime_anim_scale = 128 / 16  #  = 8

        slime_anim_timer = 0
        slime_frame_time = 1 / 4  # milli seconds
        current_anim_frame = 0
        #### ##### #### ####

        while not pr.window_should_close():
            self.input_state.pull_input()

            #### INPUT TEST
            if input_state.pressed_key_w:
                print("north")
            if input_state.pressed_key_d:
                print("east")
            if input_state.pressed_key_s:
                print("south")
            if input_state.pressed_key_a:
                print("west")
            #### END INPUT TEST

            #### SLIME ANIM ####
            slime_anim_timer += pr.get_frame_time()

            if slime_anim_timer >= slime_frame_time:
                slime_anim_timer = 0
                current_anim_frame = (current_anim_frame + 1) % len(slime_frames)

            frame_src = slime_frames[current_anim_frame]

            pos_x = 200
            pos_y = 200

            frame_dest = pr.Rectangle(
                pos_x,
                pos_y,
                frame_src.width * slime_anim_scale,
                frame_src.height * slime_anim_scale,
            )

            pr.draw_texture_pro(
                slime_anim, frame_src, frame_dest, pr.Vector2(0, 0), 0, pr.WHITE
            )
            #### ##### #### ####

            renderer.render_system(world, input_state)

        renderer.unload()
