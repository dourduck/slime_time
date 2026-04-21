from dataclasses import dataclass
import render as ren
import input as inp
import world as wor


@dataclass
class GlobalState:
    world: wor.World
    renderer: ren.Renderer
    input_state: inp.InputState
