#!/usr/bin/env python3
from input import InputState
from world import World
from render import Renderer
from global_state import GlobalState
from game import Game


def main():
    _world = World()
    _renderer = Renderer()
    _input_state = InputState()

    _global_state = GlobalState(
        world=_world, renderer=_renderer, input_state=_input_state
    )

    _game = Game(_global_state)
    _game.loop()


if __name__ == "__main__":
    main()
