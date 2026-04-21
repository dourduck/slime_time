import world as wor
import input as inp
import render as ren
import pyray as pr


class Game:
    def __init__(
        self, world: wor.World, input_state: inp.InputState, renderer: ren.Renderer
    ):
        self.world = world
        self.input_state = input_state
        self.renderer = renderer

    def loop(self):
        renderer = self.renderer
        input_state = self.input_state
        world = self.world

        renderer.create_raylib_window()

        #### RENDER TEST
        tex_tile_grass_id = renderer.load_texture("../art/iso_tile_grass.png")

        desired_tile_w = 128
        tile_src_w = 32
        tile_src_h = 32
        tile_src_x = 1
        tile_src_y = 1
        tile_scale = desired_tile_w / tile_src_w
        tile_tex_id = tex_tile_grass_id

        for i in range(4):
            tile_entity = world.create_tile_entity()
            pos_x = int(i * (tile_src_w * tile_scale))
            pos_y = 0

            tile_entity.add_texture(tile_tex_id)
            tile_entity.add_position(pos_x, pos_y)
            tile_entity.add_scale(tile_scale)
            tile_entity.add_texture_src_rect(
                tile_src_x, tile_src_y, tile_src_w, tile_src_h
            )
        #### END RENDER TEST

        while not pr.window_should_close():
            inp.pull_input(input_state)

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
