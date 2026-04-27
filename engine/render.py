from dataclasses import dataclass
import world as wor
import input as inp
import pyray as pr
import numpy as np
import math


@dataclass
class RenderConfig:
    screen_w: int = 1920
    screen_h: int = 1080
    game_title: str = "game"
    exit_key: int = 81  # (81 == pr.KeyboardKey.KEY_Q)


class Renderer:
    def __init__(self):
        self.textures: list[pr.Texture] = []
        self.config = RenderConfig()
        self.camera: pr.Camera2D | None = None

    def load_texture(self, path: str) -> int:
        tex = pr.load_texture(path)
        self.textures.append(tex)
        return len(self.textures) - 1

    def unload(self):
        for tex in self.textures:
            pr.unload_texture(tex)

    def draw_textures(self, wrld: wor.World, input_state: inp.InputState):
        assert self.camera
        camera = self.camera

        count = wrld.count
        depth = wrld.position_y[:count]
        indices = np.argsort(depth)

        for id in indices:
            tid = wrld.texture_id[id]
            tex = self.textures[tid]

            origin = pr.Vector2(0, 0)
            src = pr.Rectangle(0, 0, 0, 0)
            dest = pr.Rectangle(0, 0, 0, 0)

            src.x = wrld.src_x[id].item()
            src.y = wrld.src_y[id].item()
            src.width = wrld.src_w[id].item()
            src.height = wrld.src_h[id].item()

            dest.x = wrld.position_x[id].item()
            dest.y = wrld.position_y[id].item()
            dest.width = (wrld.src_w[id] * wrld.scale[id]).item()
            dest.height = (wrld.src_h[id] * wrld.scale[id]).item()
            rotation = wrld.rotation[id].item()

            pr.draw_texture_pro(
                tex,
                src,
                dest,
                origin,
                rotation,
                pr.WHITE,
            )  # type: ignore

            tile_w = 180
            tile_h = 180
            half_w = tile_w / 2
            quarter_h = tile_h / 4

            mx = input_state.mouse_position_x
            my = input_state.mouse_position_y

            wm = pr.get_screen_to_world_2d((mx, my), camera)
            wx, wy = int(wm.x), int(wm.y)

            gx = (wx / half_w + wy / quarter_h) / 2
            gy = (wy / quarter_h - wx / half_w) / 2

            # TODO: pass in grid resolution
            grid_resolution = 10
            grid_resolution_half = grid_resolution // 2

            gx += grid_resolution_half  # half of grid_resolution
            gy += grid_resolution_half  # half of grid_resolution

            xx = int(math.floor(gx))
            yy = int(math.floor(gy))

            if xx == -1:
                xx = 0
            elif xx == grid_resolution:
                xx = grid_resolution - 1
            if yy == -1:
                yy = 0
            elif yy == grid_resolution:
                yy = grid_resolution - 1

            # print(f"wx: {wx}, wy: {wy}")
            # print(f"xx: {xx}, yy: {yy}")

            qx = int((xx - yy) * half_w)
            qy = int((xx + yy - (grid_resolution - 1)) * quarter_h - quarter_h)

            if 0 <= xx < grid_resolution and 0 <= yy < grid_resolution:
                pr.draw_circle(qx, qy, 8, pr.RED)
            pr.draw_circle(wx, wy, 8, pr.SKYBLUE)
            # pr.draw_circle(int(dest.x + 90), int(dest.y + 45), 8, pr.RED)

    def render_system(self, wrld: wor.World, input_state: inp.InputState):
        pr.begin_drawing()
        pr.clear_background(pr.GRAY)
        assert self.camera
        pr.begin_mode_2d(self.camera)

        self.draw_textures(wrld, input_state)

        pr.end_mode_2d()
        # pr.draw_circle(
        #     (self.config.screen_w // 2),
        #     (self.config.screen_h // 2),
        #     4,
        #     pr.BLUE,
        # )

        pr.end_drawing()

    def create_raylib_window(self):
        screen_w = self.config.screen_w
        screen_h = self.config.screen_h
        game_title = self.config.game_title
        exit_key = self.config.exit_key

        pr.init_window(screen_w, screen_h, game_title)

        self.camera = pr.Camera2D()

        self.camera.zoom = 1
        self.camera.offset = pr.Vector2(0, 0)
        self.camera.rotation = 0
        self.camera.target = pr.Vector2(0, 0)
        self.camera.target = pr.Vector2(-(screen_w / 2), -(screen_h / 2))

        pr.set_target_fps(60)
        pr.set_exit_key(exit_key)


####
