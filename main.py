from enum import Enum
from copy import deepcopy


class Location(Enum):
    LEFT_BANK = 'left bank'
    RIGHT_BANK = 'right bank'

    @property
    def other(self) -> "Location":
        return self.RIGHT_BANK if self is self.LEFT_BANK else self.LEFT_BANK


class Item(Enum):
    WOLF = 'wolf'
    GOAT = 'goat'
    CABBAGE = 'cabbage'

    def __lt__(self, other) -> bool:
        """This method is used to be able to sort the Item objects inside an array"""
        return self.value[0] < other.value[0]


class State:

    def __init__(
            self,
            current_bank: list[Item],
            other_bank: list[Item],
            boat_position: Location,
            last_item: Item | None
    ):
        self._current_bank = current_bank
        self._other_bank = other_bank
        self._boat_position = boat_position
        self._last_item = last_item

    def __repr__(self) -> str:
        return f"State(" \
               f"current_bank: {self._current_bank}, " \
               f"other_bank: {self._other_bank}, " \
               f"boat_position: {self._boat_position}, " \
               f"last_item: {self._last_item})"

    def __eq__(self, other) -> bool:
        if isinstance(other, State):
            conditions = (
                sorted(self._current_bank) == sorted(other._current_bank),
                sorted(self._other_bank) == sorted(other._other_bank),
                self.boat_position == other.boat_position,
            )
            return all(conditions)

    def __hash__(self) -> int:
        """This method is for being able to remove duplicate State objects by calling set() on an array of
        State objects"""
        return 0

    def current_state(self) -> "State":
        if self.is_valid:
            return deepcopy(self)
        raise ValueError

    @staticmethod
    def initial_state() -> "State":
        """The classical beginning state of this riddle"""
        return State(
            current_bank=[Item.GOAT, Item.CABBAGE, Item.WOLF],
            other_bank=[],
            boat_position=Location.LEFT_BANK,
            last_item=None
        )

    @property
    def is_valid(self) -> bool:
        """The state is valid in the following cases:
            - it consists of exactly 3 non-duplicate Item objects shared between two banks
            - current bank must contain the last item (in case there is a last item)
            - other bank can't be invalid as we can't row away from an invalid bank"""
        conditions = (
            len([*self._current_bank, *self._other_bank]) == len({*self._current_bank, *self._other_bank}) == 3,
            self._last_item in self._current_bank if self._last_item is not None else True,
            BankValidator.is_stable(self._other_bank)
        )
        return all(conditions)

    @property
    def last_item(self) -> Item | None:
        return deepcopy(self._last_item)

    @property
    def current_bank(self) -> list[Item]:
        return deepcopy(self._current_bank)

    @property
    def other_bank(self) -> list[Item]:
        return deepcopy(self._other_bank)

    @property
    def boat_position(self) -> Location:
        return deepcopy(self._boat_position)

    @property
    def is_over(self) -> bool:
        return self._boat_position == Location.RIGHT_BANK and len(self._other_bank) == 0


class BankValidator:

    @staticmethod
    def is_stable(bank: list[Item]) -> bool:
        valid_conditions = (
            Item.GOAT not in bank or Item.CABBAGE not in bank,
            Item.GOAT not in bank or Item.WOLF not in bank,
        )

        return all(valid_conditions)


class NewStateFinder:

    def __init__(self, state: State):
        self._state = state
        self._all_valid_new_states = []

    @property
    def all_valid_new_states(self) -> list[State]:
        return deepcopy(self._all_valid_new_states)

    @property
    def empty_move_is_winning(self) -> bool:
        """If we do not check whether rowing to the other bank without anything is winning in two moves,
        the game always prefers taking an item, and we are stuck in an infinite loop"""
        valid_conditions = (
            self._state.boat_position == Location.RIGHT_BANK,
            BankValidator.is_stable(self._state.current_bank),
            len(self._state.current_bank) == 2
        )
        return all(valid_conditions)

    def empty_move(self) -> None:
        """Empty move is only available if our last move was not empty. Two consecutive empty moves are equal to
        not moving at all."""
        if self._state.last_item is not None:
            if BankValidator.is_stable(self._state.current_bank):
                new_state = State(
                    current_bank=self._state.other_bank,
                    other_bank=self._state.current_bank,
                    boat_position=self._state.boat_position.other,
                    last_item=None
                )
                self._all_valid_new_states.append(new_state)

    def item_moves(self) -> None:
        """We can only take an item with us if we did not take the same item last turn. Taking the same item
        for two consecutive turns is equal to not moving at all."""
        for current_item in self._state.current_bank:
            if current_item != self._state.last_item:
                current_bank = [item for item in self._state.current_bank if item != current_item]
                if BankValidator.is_stable(current_bank):
                    other_bank = self._state.other_bank
                    other_bank.append(current_item)
                    new_state = State(
                        current_bank=other_bank,
                        other_bank=current_bank,
                        boat_position=self._state.boat_position.other,
                        last_item=current_item
                    )
                    self._all_valid_new_states.append(new_state)

    def get_new_states(self) -> list[State]:
        self.empty_move()
        if not self.empty_move_is_winning:
            self.item_moves()
        return self.all_valid_new_states


class Engine:

    def __init__(self, initial_state: State | None = None):
        if initial_state is None:
            initial_state = State.initial_state()

        self._initial_state = initial_state
        self._all_states: list[list[State]] = []

    @property
    def all_states(self) -> list[list[State]]:
        return deepcopy(self._all_states)

    @property
    def all_states_length(self) -> int:
        return len(self._all_states)

    def run(self) -> None:
        self._all_states.append([self._initial_state])

        idx = 0
        while True:
            new_states = []
            for state in self._all_states[idx]:
                if not state.is_over:
                    new_states += [new_state for new_state in NewStateFinder(state).get_new_states()]
            if not new_states:
                break
            self._all_states.append(new_states)
            idx += 1


class Utility:

    @staticmethod
    def is_longer_than_one(iterable) -> bool:
        return len(iterable) > 1

    @staticmethod
    def remove_duplicates(array) -> set:
        return set(array)

    @staticmethod
    def pluralize(word: str, count: int) -> str:
        output_string = f'{count} {word}'
        if count != 1:
            return output_string + 's'
        return output_string


class StoryTeller:

    def __init__(self, engine: Engine):
        self._engine = engine

    def tell_story(self) -> None:
        for idx in range(self._engine.all_states_length):
            result = Utility.remove_duplicates(self._engine.all_states[idx])
            print(f'Turn {idx + 1}.')
            print()

            for count, state in enumerate(result, 1):
                if Utility.is_longer_than_one(result):  # if there is more than 1 possible move available
                    print(f'Path {count}:')
                    print()

                print(f'We are currently on the {state.boat_position.value}.')
                print(
                    f'We have {Utility.pluralize("item", len(state.current_bank))} here: '
                    f'{", ".join(f"the {item.value}" for item in state.current_bank)}.'
                )

                try:
                    last_items = [res.last_item.value for res in self._engine.all_states[idx + 1] if
                                  res.last_item in state.current_bank]
                    last_items = list(Utility.remove_duplicates(last_items))

                    if last_items:
                        print(f'I see {Utility.pluralize("way", len(last_items))} to proceed:')
                        print(f'We can take {" or ".join(f"the {item}" for item in last_items)} with us.')
                        empty = False
                    else:
                        print('I see 1 way to proceed:')
                        print(f'We should row back to the other bank without taking any items with us.')
                        empty = True
                    print()

                except IndexError:  # no next moves available
                    print('We are done! We can walk home.')
                    print()
                    break

                if empty:
                    last_items = 'nothing'
                else:
                    if len(last_items) == 1:
                        last_items = f'the {last_items[0]}'
                    else:
                        last_items = ' and then '.join(f"the {item} (Path {path})"
                                                       for path, item in enumerate(last_items, 1))

                print(f'Rowing over to the {state.boat_position.other.value} with {last_items}...')
                print()


if __name__ == '__main__':
    story_engine = Engine()
    story_engine.run()

    story_teller = StoryTeller(engine=story_engine)
    story_teller.tell_story()
