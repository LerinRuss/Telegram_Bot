from game.appearance import AppearanceState, appearance_pair_factory


def test_both_different__raise():
    (first_essence, second_essence) = appearance_pair_factory(AppearanceState.UP, AppearanceState.DOWN)

    second_essence.raise_please()

    assert second_essence.obtain() is AppearanceState.UP

    assert first_essence.obtain() is AppearanceState.LOWERED
    assert first_essence.obtain() is AppearanceState.DOWN


def test_both_different__lower():
    (first_essence, second_essence) = appearance_pair_factory(AppearanceState.UP, AppearanceState.DOWN)

    first_essence.lower()

    assert first_essence.obtain() is AppearanceState.DOWN

    assert second_essence.obtain() is AppearanceState.RAISED
    assert second_essence.obtain() is AppearanceState.UP


def test_both_different__raise_to_limit():
    (first_essence, second_essence) = appearance_pair_factory(AppearanceState.DOWN, AppearanceState.UP)

    for _ in range(2):
        second_essence.raise_please()

        assert first_essence.obtain() is AppearanceState.DOWN
        assert second_essence.obtain() is AppearanceState.UP


def test_both_different__lower_to_limit():
    (first_essence, second_essence) = appearance_pair_factory(AppearanceState.DOWN, AppearanceState.UP)

    for _ in range(2):
        first_essence.lower()

        assert first_essence.obtain() is AppearanceState.DOWN
        assert second_essence.obtain() is AppearanceState.UP


def test_both_down__raise():
    (first_essence, second_essence) = appearance_pair_factory(AppearanceState.DOWN, AppearanceState.DOWN)

    first_essence.raise_please()

    assert first_essence.obtain() is AppearanceState.UP

    assert second_essence.obtain() is AppearanceState.RAISED
    assert second_essence.obtain() is AppearanceState.UP


def test_both_up__lower():
    (first_essence, second_essence) = appearance_pair_factory(AppearanceState.UP, AppearanceState.UP)

    first_essence.lower()

    assert first_essence.obtain() is AppearanceState.DOWN

    assert second_essence.obtain() is AppearanceState.LOWERED
    assert second_essence.obtain() is AppearanceState.DOWN


def test_both_down__lower_to_limit():
    (first_essence, second_essence) = appearance_pair_factory(AppearanceState.DOWN, AppearanceState.DOWN)

    first_essence.lower()

    assert first_essence.obtain() is AppearanceState.DOWN

    assert second_essence.obtain() is AppearanceState.RAISED
    assert second_essence.obtain() is AppearanceState.UP

    first_essence.lower()

    assert first_essence.obtain() is AppearanceState.DOWN

    assert second_essence.obtain() is AppearanceState.UP


def test_both_up__raise_to_limit():
    (first_essence, second_essence) = appearance_pair_factory(AppearanceState.UP, AppearanceState.UP)

    first_essence.raise_please()

    assert first_essence.obtain() is AppearanceState.UP

    assert second_essence.obtain() is AppearanceState.LOWERED
    assert second_essence.obtain() is AppearanceState.DOWN

    first_essence.raise_please()

    assert first_essence.obtain() is AppearanceState.UP

    assert second_essence.obtain() is AppearanceState.DOWN
