import pyray as pr
from dataclasses import dataclass, field


@dataclass
class InputState:
    mouse_position_x: int = field(default_factory=int)
    mouse_position_y: int = field(default_factory=int)

    pressed_key_w: bool = field(default_factory=bool)
    pressed_key_d: bool = field(default_factory=bool)
    pressed_key_s: bool = field(default_factory=bool)
    pressed_key_a: bool = field(default_factory=bool)


def pull_input(state: InputState):
    current_key_pressed = pr.get_key_pressed()

    key_w = pr.KeyboardKey.KEY_W
    key_d = pr.KeyboardKey.KEY_D
    key_s = pr.KeyboardKey.KEY_S
    key_a = pr.KeyboardKey.KEY_A

    state.pressed_key_w = current_key_pressed == key_w
    state.pressed_key_d = current_key_pressed == key_d
    state.pressed_key_s = current_key_pressed == key_s
    state.pressed_key_a = current_key_pressed == key_a

    state.mouse_position_x = pr.get_mouse_x()
    state.mouse_position_y = pr.get_mouse_y()


# def tile_mouse_input(
#     world: World,
#     iso_data: IsoData,
#     # , camera: pr.Camera2D
# ):
#     mouse_pos = pr.get_mouse_position()
#     # mouse_pos_world = pr.get_screen_to_world_2d(mouse_pos, camera)
#     # wx, wy = mouse_pos_world.x, mouse_pos_world.y
#     mx, my = mouse_pos.x, mouse_pos.y
#
#     tile_width = iso_data.tile_w
#     tile_height = iso_data.tile_h
#
#     nx = mx / (tile_width / 2)
#     ny = my / (tile_height / 2)
#
#     gx = (nx + ny) / 2
#     gy = (ny - nx) / 2
#
#     tx = floor(gx)
#     ty = floor(gy)
#
#     cx, cy = iso_data.iso_to_screen(tx, ty)
#
#     dx = mx - cx
#     dy = my - cy
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
#     x, y, r, c = int(tx * tile_width), int(ty * tile_height), 8, pr.GREEN
#     pr.draw_circle(x, y, r, c)
#
#     return (tx, ty)


#### #### ####
