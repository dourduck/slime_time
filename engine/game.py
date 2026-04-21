import global_state as glb

import world as wor

import pyray as pr


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

        desired_tile_w = 128
        tile_src_w = 32
        tile_src_h = 32
        tile_src_x = 1
        tile_src_y = 1
        tile_scale = desired_tile_w / tile_src_w

        for i in range(4):
            tile_entity = world.create_tile_entity()
            pos_x = int(i * (tile_src_w * tile_scale))
            pos_y = 0

            tile_entity.add_texture(tile_tex_grass_id)
            tile_entity.add_position(pos_x, pos_y)
            tile_entity.add_scale(tile_scale)
            tile_entity.add_texture_src_rect(
                tile_src_x, tile_src_y, tile_src_w, tile_src_h
            )
        #### END RENDER TEST

        #### Kind test
        ent: wor.Entity = world.entities[world.entity_tag_tile.pop()]
        kind = wor.EntityKind.TILE
        kind |= wor.EntityKind.ENEMY
        ent.set_kind(kind)

        for eid in world.entity_tag_tile:
            print(f"tile entity id: {eid}")
        for eid in world.entity_tag_enemy:
            print(f"enemy entity id: {eid}")
        ####

        #### data mutation via tag test
        idx = list((world.entity_tag_tile.intersection(world.entity_tag_enemy)))
        world.position_x[idx] -= 400
        world.position_y[idx] -= 200
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
