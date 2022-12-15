from game.scene_object import Character, Bucket
from game.game import candle_command_pair_factory, fireplace_wood_command_pair_factory
from game.appearance import AppearanceState
from game import *

import pytest


def test_up_and_down_candles_without_bucket_and_lighter__blow_out_command_and_observation_after_command():
    first_candle, second_candle = candle_command_pair_factory(AppearanceState.UP, AppearanceState.DOWN)
    character = Character()

    first_state, first_top_text, first_commands = first_candle.update(character)
    second_state, second_top_text, second_commands = second_candle.update(character)

    assert first_state is AppearanceState.UP
    assert second_state is AppearanceState.DOWN

    assert first_top_text is CANDLE_COME_UP_UP_TEXT
    assert second_top_text is CANDLE_TOP_TEXT_DOWN

    assert len(first_commands) == 1
    assert len(second_commands) == 0

    assert first_commands[0].cmd_text is CANDLE_BLOW_OUT_TEXT
    assert first_commands[0].res_text is CANDLE_BLOW_OUT_RESULT_TEXT

    blow_out_command = first_commands[0].cmd
    blow_out_command()

    first_state_after_command, first_top_text_after_command, first_commands_after_command = \
        first_candle.update(character)
    second_state_after_command, second_top_text_after_command, second_commands_after_command = \
        second_candle.update(character)

    assert first_state_after_command is AppearanceState.DOWN
    assert second_state_after_command is AppearanceState.RAISED

    assert first_top_text_after_command is CANDLE_TOP_TEXT_DOWN
    assert second_top_text_after_command is CANDLE_COME_UP_RAISED_TEXT

    assert len(first_commands_after_command) == 0
    assert len(second_commands_after_command) == 1

    assert second_commands_after_command[0].cmd_text is CANDLE_BLOW_OUT_TEXT
    assert second_commands_after_command[0].res_text is CANDLE_BLOW_OUT_RESULT_TEXT

    second_state_after_seen, second_top_text_after_seen, second_commands_after_seen = \
        second_candle.update(character)

    assert second_state_after_seen is AppearanceState.UP
    assert second_top_text_after_seen is CANDLE_COME_UP_UP_TEXT
    assert len(second_commands_after_seen) == 1
    assert second_commands_after_seen[0].cmd_text is CANDLE_BLOW_OUT_TEXT
    assert second_commands_after_seen[0].res_text is CANDLE_BLOW_OUT_RESULT_TEXT


def test_character_without_bucket__cannot_blow_out_fireplace_wood():
    first_wood, _ = fireplace_wood_command_pair_factory(AppearanceState.UP, AppearanceState.DOWN)
    character = Character()
    character.bucket = None

    _, _, first_commands = first_wood.update(character)

    assert len(first_commands) == 0


def test_character_with_bucket_but_without_content__cannot_blow_out_fireplace_wood():
    first_wood, _ = fireplace_wood_command_pair_factory(AppearanceState.UP, AppearanceState.DOWN)
    character = Character()
    character.bucket = Bucket()

    _, _, first_commands = first_wood.update(character)

    assert len(first_commands) == 0


@pytest.mark.parametrize('bucket_content', [Bucket.Content.SNOW, Bucket.Content.WATER])
def test_character_with_snow_or_waiter_in_bucket__blow_out_fireplace_wood(bucket_content):
    first_wood, second_wood = fireplace_wood_command_pair_factory(AppearanceState.UP, AppearanceState.DOWN)
    character = Character()
    character.bucket = Bucket(bucket_content)

    _, _, first_commands = first_wood.update(character)
    second_wood.update(character)

    assert len(first_commands) == 1
    assert first_commands[0].cmd_text is FIREPLACE_WOOD_BLOW_OUT_WITH_SNOW_TEXT
    assert first_commands[0].res_text is FIREPLACE_WOOD_BLOW_OUT_WITH_SNOW_RESULT_TEXT

    first_commands[0].cmd()

    first_state_after_cmd, first_top_text_after_cmd, first_commands_after_cmd = first_wood.update(character)
    second_state_after_cmd, second_top_text_after_cmd, second_commands_after_cmd = first_wood.update(character)

    assert first_state_after_cmd is AppearanceState.DOWN
    assert second_state_after_cmd is AppearanceState.DOWN

    assert first_top_text_after_cmd is FIREPLACE_WOOD_TOP_TEXT_WET
    assert second_top_text_after_cmd is FIREPLACE_WOOD_COME_UP_DOWN_TEXT

    assert len(first_commands_after_cmd) == 1
    assert len(second_commands_after_cmd) == 0

    assert first_commands_after_cmd[0].cmd_text is FIREPLACE_WOOD_RESET_EFFECT_TEXT
    assert first_commands_after_cmd[0].res_text is FIREPLACE_WOOD_RESET_EFFECT_RESULT_TEXT
