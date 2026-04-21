#!/usr/bin/env python3
from __future__ import annotations

import input as inp
import world as wor
import render as ren
import game as gam
import global_state as glb


def main():
    world = wor.World()
    renderer = ren.Renderer()
    input_state = inp.InputState()

    global_state = glb.GlobalState(
        world=world, renderer=renderer, input_state=input_state
    )

    game = gam.Game(global_state)
    game.loop()


if __name__ == "__main__":
    main()
