import enum

from typing import Union


class AppearanceState(enum.Enum):
    DOWN = 1
    LOWERED = 2
    RAISED = 3
    UP = 4


class _AppearanceControl:
    def __init__(self, current_state: AppearanceState):
        self._current_state = current_state

    def _up(self) -> None:
        self._current_state = AppearanceState.UP

    def _down(self) -> None:
        self._current_state = AppearanceState.DOWN

    def _raise_please(self) -> None:
        if self._current_state is AppearanceState.UP:
            return

        if self._current_state is AppearanceState.LOWERED:
            self._current_state = AppearanceState.UP

            return

        self._current_state = AppearanceState.RAISED

    def _lower(self) -> None:
        if self._current_state is AppearanceState.DOWN:
            return

        if self._current_state is AppearanceState.RAISED:
            self._current_state = AppearanceState.DOWN

            return

        self._current_state = AppearanceState.LOWERED

    def obtain(self) -> AppearanceState:
        res = self._current_state

        if self._current_state is AppearanceState.RAISED:
            self._current_state = AppearanceState.UP
        elif self._current_state is AppearanceState.LOWERED:
            self._current_state = AppearanceState.DOWN

        return res


def try_raise(essence: _AppearanceControl) -> None:
    if essence._current_state is AppearanceState.LOWERED or essence._current_state is AppearanceState.DOWN:

        essence._raise_please()
    else:
        essence._lower()


def try_lower(essence: _AppearanceControl) -> None:
    if essence._current_state is AppearanceState.RAISED or essence._current_state is AppearanceState.UP:

        essence._lower()
    else:
        essence._raise_please()


class _SimpleMediator:
    def __init__(self, first_appearance: _AppearanceControl, second_appearance: _AppearanceControl):
        self._first_appearance = first_appearance
        self._second_appearance = second_appearance

    def raise_first(self) -> None:
        self._first_appearance._up()
        try_raise(self._second_appearance)

    def raise_second(self) -> None:
        self._second_appearance._up()
        try_raise(self._first_appearance)

    def lower_first(self) -> None:
        self._first_appearance._down()
        try_lower(self._second_appearance)

    def lower_second(self) -> None:
        self._second_appearance._down()
        try_lower(self._first_appearance)


class AppearanceObject:
    def __init__(self, _raise_delegated, _lower_delegated, _obtain_delegated):
        self._raise_delegated = _raise_delegated
        self._lower_delegated = _lower_delegated
        self._obtain_delegated = _obtain_delegated

    def raise_please(self, *args, **kwargs) -> None:
        self._raise_delegated(*args, **kwargs)

    def lower(self, *args, **kwargs) -> None:
        self._lower_delegated(*args, **kwargs)

    def obtain(self, *args, **kwargs) -> AppearanceState:
        return self._obtain_delegated(*args, **kwargs)


class GameSource:
    def __init__(self, resource: Union[any, None], appearance: _AppearanceControl):
        if resource is not None:
            assert appearance._current_state is AppearanceState.UP
        else:
            assert appearance._current_state is AppearanceState.DOWN

        self._mediator: Union[SourceMediator, None] = None
        self.resource: Union[any, None] = resource
        self._appearance = appearance

    def pick_up_resource(self) -> Union[any, None]:
        if self.resource is None:
            #   TODO log
            return None

        res = self.resource
        self.resource = None
        self._appearance._down()
        self._mediator._remove_resource(self)

        return res

    def put_down_resource(self, resource: any):
        if resource is None:
            #   TODO log
            return

        self.resource = resource
        self._appearance._up()
        self._mediator._spread_resource(self, resource)

    def obtain(self) -> AppearanceState:
        return self._appearance.obtain()

    def _remove_resource(self):
        self.resource = None
        self._appearance._lower()

    def _put_resource(self, resource: any):
        self.resource = resource
        self._appearance._raise_please()


class SourceMediator:
    def __init__(self, first_source: GameSource, second_source: GameSource):
        self._first_source = first_source
        self._second_source = second_source

        self._first_source._mediator = self
        self._second_source._mediator = self

    def _spread_resource(self, source: GameSource, resource: any):
        if source is not self._first_source:
            self._first_source._put_resource(resource)
        else:
            self._second_source._put_resource(resource)

    def _remove_resource(self, source: GameSource):
        if source is not self._first_source:
            self._first_source._remove_resource()
        else:
            self._second_source._remove_resource()


def appearance_pair_factory(first_essence_init_state: AppearanceState, second_essence_init_state: AppearanceState) -> \
        (AppearanceObject, AppearanceObject):
    first_appearance_control = _AppearanceControl(first_essence_init_state)
    second_appearance_control = _AppearanceControl(second_essence_init_state)

    mediator = _SimpleMediator(first_appearance_control, second_appearance_control)

    first_appearance = AppearanceObject(
        lambda: mediator.raise_first(),
        lambda: mediator.lower_first(),
        first_appearance_control.obtain)
    second_appearance = AppearanceObject(
        lambda: mediator.raise_second(),
        lambda: mediator.lower_second(),
        second_appearance_control.obtain)

    return first_appearance, second_appearance


def source_pair_factory(first_source_state: AppearanceState, second_source_state: AppearanceState, resource=None):
    assert first_source_state == second_source_state

    first_appearance_control = _AppearanceControl(first_source_state)
    second_appearance_control = _AppearanceControl(second_source_state)

    first_game_source = GameSource(resource, first_appearance_control)
    second_game_source = GameSource(resource, second_appearance_control)

    SourceMediator(first_game_source, second_game_source)

    return first_game_source, second_game_source
