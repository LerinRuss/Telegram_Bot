from game.appearance import AppearanceState, appearance_pair_factory, source_pair_factory
import pytest


class TestStandard:
    def test_both_different__raise(self):
        (first_essence, second_essence) = appearance_pair_factory(AppearanceState.UP, AppearanceState.DOWN)

        second_essence.raise_please()

        assert second_essence.obtain() is AppearanceState.UP

        assert first_essence.obtain() is AppearanceState.LOWERED
        assert first_essence.obtain() is AppearanceState.DOWN

    def test_both_different__lower(self):
        (first_essence, second_essence) = appearance_pair_factory(AppearanceState.UP, AppearanceState.DOWN)

        first_essence.lower()

        assert first_essence.obtain() is AppearanceState.DOWN

        assert second_essence.obtain() is AppearanceState.RAISED
        assert second_essence.obtain() is AppearanceState.UP

    def test_both_different__raise_to_limit(self):
        (first_essence, second_essence) = appearance_pair_factory(AppearanceState.DOWN, AppearanceState.UP)

        for _ in range(2):
            second_essence.raise_please()

            assert first_essence.obtain() is AppearanceState.DOWN
            assert second_essence.obtain() is AppearanceState.UP

    def test_both_different__lower_to_limit(self):
        (first_essence, second_essence) = appearance_pair_factory(AppearanceState.DOWN, AppearanceState.UP)

        for _ in range(2):
            first_essence.lower()

            assert first_essence.obtain() is AppearanceState.DOWN
            assert second_essence.obtain() is AppearanceState.UP

    def test_both_down__raise(self):
        (first_essence, second_essence) = appearance_pair_factory(AppearanceState.DOWN, AppearanceState.DOWN)

        first_essence.raise_please()

        assert first_essence.obtain() is AppearanceState.UP

        assert second_essence.obtain() is AppearanceState.RAISED
        assert second_essence.obtain() is AppearanceState.UP

    def test_both_up__lower(self):
        (first_essence, second_essence) = appearance_pair_factory(AppearanceState.UP, AppearanceState.UP)

        first_essence.lower()

        assert first_essence.obtain() is AppearanceState.DOWN

        assert second_essence.obtain() is AppearanceState.LOWERED
        assert second_essence.obtain() is AppearanceState.DOWN

    def test_both_down__lower_to_limit(self):
        (first_essence, second_essence) = appearance_pair_factory(AppearanceState.DOWN, AppearanceState.DOWN)

        first_essence.lower()

        assert first_essence.obtain() is AppearanceState.DOWN

        assert second_essence.obtain() is AppearanceState.RAISED
        assert second_essence.obtain() is AppearanceState.UP

        first_essence.lower()

        assert first_essence.obtain() is AppearanceState.DOWN

        assert second_essence.obtain() is AppearanceState.UP

    def test_both_up__raise_to_limit(self):
        (first_essence, second_essence) = appearance_pair_factory(AppearanceState.UP, AppearanceState.UP)

        first_essence.raise_please()

        assert first_essence.obtain() is AppearanceState.UP

        assert second_essence.obtain() is AppearanceState.LOWERED
        assert second_essence.obtain() is AppearanceState.DOWN

        first_essence.raise_please()

        assert first_essence.obtain() is AppearanceState.UP

        assert second_essence.obtain() is AppearanceState.DOWN


class TestSource:
    def test_different_state__error(self):
        with pytest.raises(AssertionError):
            _, _ = source_pair_factory(AppearanceState.DOWN, AppearanceState.UP)

    def test_both_up_but_none_resource__error(self):
        with pytest.raises(AssertionError):
            _, _ = source_pair_factory(AppearanceState.UP, AppearanceState.UP)

    def test_both_down_but_resource_present__error(self):
        with pytest.raises(AssertionError):
            _, _ = source_pair_factory(AppearanceState.DOWN, AppearanceState.DOWN, object())

    def test_both_down_put_object__must_both_have_this_object(self):
        first, second = source_pair_factory(AppearanceState.DOWN, AppearanceState.DOWN)

        assert first.obtain() is second.obtain() is AppearanceState.DOWN

        resource = object()
        first.put_down_resource(resource)

        assert second.obtain() is AppearanceState.RAISED

        assert first.obtain() is second.obtain() is AppearanceState.UP
        assert first.resource is second.resource is resource

        assert second.obtain() is AppearanceState.UP

    def test_both_up_and_pick_up_resource__both_empty_after_action(self):
        origin_resource = object()
        first, second = source_pair_factory(AppearanceState.UP, AppearanceState.UP, origin_resource)

        assert first.obtain() is second.obtain() is AppearanceState.UP
        assert first.resource is second.resource is origin_resource

        picked_resource = first.pick_up_resource()

        assert first.resource is second.resource is None
        assert picked_resource is origin_resource

        assert second.obtain() is AppearanceState.LOWERED
        assert first.obtain() is second.obtain() is AppearanceState.DOWN

        assert second.obtain() is AppearanceState.DOWN

    def test_resourced_picked_but_second_not_obtained_and_again_put_to_the_first__second_not_changed(self):
        first, second = source_pair_factory(AppearanceState.UP, AppearanceState.UP, object())
        first.pick_up_resource()

        resource = object()
        first.put_down_resource(resource)

        assert first.resource is second.resource is resource
        assert first.obtain() is second.obtain() is AppearanceState.UP
