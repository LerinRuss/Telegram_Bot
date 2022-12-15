import abc

from typing import Union
from game.appearance import AppearanceObject, AppearanceState, appearance_pair_factory
from game.scene_object import DialogCommand, CommandObject, EffectState, Character, Bucket
from game import *


class StandardCommandObject(CommandObject):
    def __init__(self, essence: AppearanceObject, text_factory: Callable[[AppearanceState], str],
                 reset_effect_text: str, reset_effect_result_text: str,
                 blow_out_text: str, blow_out_result_text: str,
                 light_up_text: str, light_up_result_text: str,
                 wet_text: str, wet_result_text: str):
        super().__init__(essence, text_factory)

        self._reset_effect_text = reset_effect_text
        self._reset_effect_result_text = reset_effect_result_text
        self._blow_out_text = blow_out_text
        self._blow_out_result_text = blow_out_result_text
        self._light_up_text = light_up_text
        self._light_up_result_text = light_up_result_text
        self._wet_text = wet_text
        self._wet_result_text = wet_result_text

    def _obtain_commands(self, current_state: AppearanceState, character: Character) -> \
            list[DialogCommand]:
        reset_effect = self._reset_wet_effect_command()
        if reset_effect:
            return [DialogCommand(self._reset_effect_text, reset_effect, self._reset_effect_result_text)]

        res = []

        blow_out = self._blow_out_command(current_state)
        if blow_out:
            res.append(DialogCommand(self._blow_out_text, blow_out, self._blow_out_result_text))
        else:
            light_up = self._light_up_command(current_state, character)
            if light_up:
                res.append(DialogCommand(self._light_up_text, light_up, self._light_up_result_text))

        wet_command = self._wet_command(current_state, character)
        if wet_command:
            res.append(DialogCommand(self._wet_text, wet_command, self._wet_result_text))

        return res


def candle_action_top_text_factory(current_state: AppearanceState) -> str:
    if current_state is AppearanceState.DOWN:
        return CANDLE_TOP_TEXT_DOWN
    elif current_state is AppearanceState.LOWERED:
        return CANDLE_COME_UP_LOWERED_TEXT
    elif current_state is AppearanceState.RAISED:
        return CANDLE_COME_UP_RAISED_TEXT
    elif current_state is AppearanceState.UP:
        return CANDLE_COME_UP_UP_TEXT
    else:
        return CANDLE_COME_UP_UNKNOWN_TEXT


def fireplace_wood_action_top_text_factory(current_state: AppearanceState) -> str:
    if current_state is AppearanceState.DOWN:
        return FIREPLACE_WOOD_COME_UP_DOWN_TEXT
    elif current_state is AppearanceState.LOWERED:
        return FIREPLACE_WOOD_COME_UP_LOWERED_TEXT
    elif current_state is AppearanceState.RAISED:
        return FIREPLACE_WOOD_COME_UP_RAISED_TEXT
    elif current_state is AppearanceState.UP:
        return FIREPLACE_WOOD_COME_UP_UP_TEXT
    else:
        return FIREPLACE_WOOD_COME_UP_UNKNOWN_TEXT


def candle_command_pair_factory(first_init_state: AppearanceState, second_init_state: AppearanceState) -> \
        tuple[StandardCommandObject, StandardCommandObject]:
    first_essence, second_essence = appearance_pair_factory(first_init_state, second_init_state)
    first_candle = StandardCommandObject(first_essence,
                                         candle_action_top_text_factory,
                                         CANDLE_RESET_EFFECT_TEXT, CANDLE_RESET_EFFECT_RESULT_TEXT,
                                         CANDLE_BLOW_OUT_TEXT, CANDLE_BLOW_OUT_RESULT_TEXT,
                                         CANDLE_LIGHT_UP_TEXT, CANDLE_LIGHT_UP_RESULT_TEXT,
                                         CANDLE_WET_TEXT, CANDLE_WET_RESULT_TEXT)
    second_candle = StandardCommandObject(second_essence,
                                          candle_action_top_text_factory,
                                          CANDLE_RESET_EFFECT_TEXT, CANDLE_RESET_EFFECT_RESULT_TEXT,
                                          CANDLE_BLOW_OUT_TEXT, CANDLE_BLOW_OUT_RESULT_TEXT,
                                          CANDLE_LIGHT_UP_TEXT, CANDLE_LIGHT_UP_RESULT_TEXT,
                                          CANDLE_WET_TEXT, CANDLE_WET_RESULT_TEXT)
    return first_candle, second_candle


def fireplace_wood_command_pair_factory(first_init_state: AppearanceState, second_init_state: AppearanceState) -> \
        tuple[StandardCommandObject, StandardCommandObject]:
    first_essence, second_essence = appearance_pair_factory(first_init_state, second_init_state)
    first_fireplace_wood = StandardCommandObject(first_essence,
                                                 fireplace_wood_action_top_text_factory,
                                                 FIREPLACE_WOOD_RESET_EFFECT_TEXT, FIREPLACE_WOOD_RESET_EFFECT_RESULT_TEXT,
                                                 FIREPLACE_WOOD_BLOW_OUT_TEXT, FIREPLACE_WOOD_BLOW_OUT_RESULT_TEXT,
                                                 FIREPLACE_WOOD_LIGHT_UP_TEXT, FIREPLACE_WOOD_LIGHT_UP_RESULT_TEXT,
                                                 FIREPLACE_WOOD_WET_TEXT, FIREPLACE_WOOD_WET_RESULT_TEXT)
    second_fireplace_wood = StandardCommandObject(second_essence,
                                                  fireplace_wood_action_top_text_factory,
                                                  FIREPLACE_WOOD_RESET_EFFECT_TEXT, FIREPLACE_WOOD_RESET_EFFECT_RESULT_TEXT,
                                                  FIREPLACE_WOOD_BLOW_OUT_TEXT, FIREPLACE_WOOD_BLOW_OUT_RESULT_TEXT,
                                                  FIREPLACE_WOOD_LIGHT_UP_TEXT, FIREPLACE_WOOD_LIGHT_UP_RESULT_TEXT,
                                                  FIREPLACE_WOOD_WET_TEXT, FIREPLACE_WOOD_WET_RESULT_TEXT)
    return first_fireplace_wood, second_fireplace_wood
