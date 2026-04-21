#!/usr/bin/env python3
from __future__ import annotations

# import world as wor
# import pyray as pr

import input as inp
import world as wor
import render as ren
import game as gam


def main():
    world = wor.World()
    input_state = inp.InputState()
    renderer = ren.Renderer()
    game = gam.Game(world=world, input_state=input_state, renderer=renderer)
    game.loop()


if __name__ == "__main__":
    main()
