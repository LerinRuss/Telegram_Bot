from game.appearance import AppearanceState
from game.scene_object import Character, DialogCommand
from typing import Callable


def collect_commands(current_state: AppearanceState, character: Character,
                     *factories: Callable[[AppearanceState, Character], tuple[bool, DialogCommand]]) -> \
        list[DialogCommand]:
    res = []
    for factory in factories:
        need_stop, cmd = factory(current_state, character)

        res.append(cmd)

        if need_stop:
            break

    return res

