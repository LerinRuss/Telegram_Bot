import enum
from abc import ABC, abstractmethod
from typing import Callable, Union
from game.appearance import AppearanceState, AppearanceObject
from game import Command


class EffectState(enum.Enum):
    NOTHING = 1
    WET = 2


class Lighter:
    pass


class Bucket:
    class Content(enum.Enum):
        SNOW = 1
        WATER = 2

    def __init__(self, content=None):
        self.content = content


class Character:
    def __init__(self, lighter: Lighter = None, bucket: Bucket = None):
        self.lighter: Lighter = lighter
        self.bucket: Bucket = bucket


class DialogCommand:
    def __init__(self, cmd_text: str, cmd: Command, res_text: str):
        self.cmd_text = cmd_text
        self.cmd = cmd
        self.res_text = res_text


class CommandObject(ABC):
    def __init__(self, essence: AppearanceObject,
                 text_factory: Callable[[AppearanceState], str]):
        self._essence = essence
        self._text_factory = text_factory
        self._effect = EffectState.NOTHING

    def update(self, character: Character) -> tuple[AppearanceState, str, list[DialogCommand]]:
        current_state = self._essence.obtain()

        text = self._text_factory(current_state)
        commands = self._obtain_commands(current_state, character)

        return current_state, text, commands

    @abstractmethod
    def _obtain_commands(self, current_state: AppearanceState, character: Character) -> list[DialogCommand]:
        pass

    def _reset_wet_effect_command(self) -> Union[Command, None]:
        if self._effect is EffectState.WET:
            def reset_effect():
                self._effect = EffectState.NOTHING

            return reset_effect

        return None

    def _blow_out_command(self, current_state: AppearanceState) -> Union[Command, None]:
        if current_state is AppearanceState.UP or current_state is AppearanceState.RAISED:
            return self._essence.lower

        return None

    def _light_up_command(self, current_state: AppearanceState, character: Character) -> Union[Command, None]:
        if character.lighter and (current_state is AppearanceState.DOWN or current_state is AppearanceState.LOWERED):
            return self._essence.raise_please

        return None

    def _wet_command(self, current_state: AppearanceState, character: Character) -> Union[Command, None]:
        if character.bucket and character.bucket.content is Bucket.Content.WATER:
            def wet():
                if current_state is AppearanceState.UP or current_state is AppearanceState.RAISED:
                    self._essence.lower()
                self._effect = EffectState.WET

            return wet

        return None
