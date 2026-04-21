from dataclasses import dataclass
import world as wor
import pyray as pr
import numpy as np


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

    def draw_textures(self, wrld: wor.World):
        order = np.argsort(wrld.texture_id[: wrld.count])
        for id in order:
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

    def render_system(
        self,
        wrld: wor.World,
    ):
        pr.begin_drawing()
        pr.clear_background(pr.GRAY)
        assert self.camera
        pr.begin_mode_2d(self.camera)

        self.draw_textures(wrld)

        pr.end_mode_2d()

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

        """
        texture data class?
        just pass the renderer instance

        """

        # tex_tile_grass_id = self.load_texture("../art/iso_tile_grass.png")
        #
        # desired_tile_w = 128
        # tile_src_w = 32
        # tile_src_h = 32
        # tile_src_x = 1
        # tile_src_y = 1
        # tile_scale = desired_tile_w / tile_src_w
        # tile_tex_id = tex_tile_grass_id
        #
        # for i in range(4):
        #     tile_entity = wrld.create_tile_entity()
        #     pos_x = int(i * (tile_src_w * tile_scale))
        #     pos_y = 0
        #
        #     tile_entity.assign_texture_id(wrld, tile_tex_id)
        #     tile_entity.assign_position(wrld, pos_x, pos_y)
        #     tile_entity.assign_scale(wrld, tile_scale)
        #     tile_entity.assign_src_rect(
        #         wrld, tile_src_x, tile_src_y, tile_src_w, tile_src_h
        #     )
        ####


####
