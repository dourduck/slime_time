import global_state as glb
import pyray as pr

# import world as wor
# import numpy as np


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
        tile_tex_grass_id = renderer.load_texture("../art/iso_tile_grass.png")

        # slime_anim = renderer.load_texture("../art/slime_anim.png")  # (16x16) 4 frames
        # slime_anim_scale = 128 / 16  #  = 8

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

            renderer.render_system(world)

        renderer.unload()
