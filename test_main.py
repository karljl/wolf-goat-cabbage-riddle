import unittest
from unittest import TestCase
from main import Location, Item, State, BankValidator, NewStateFinder, Engine, Utility


class TestLocation(TestCase):

    def test_other(self):
        self.assertEqual(Location.LEFT_BANK, Location.RIGHT_BANK.other)
        self.assertEqual(Location.RIGHT_BANK, Location.LEFT_BANK.other)


class TestItem(TestCase):

    def test_lt(self):
        self.assertLess(Item.CABBAGE, Item.GOAT)
        self.assertLess(Item.GOAT, Item.WOLF)
        self.assertLess(Item.CABBAGE, Item.WOLF)


class TestState(TestCase):
    states = [
        State(  # 0
            current_bank=[Item.WOLF, Item.CABBAGE, Item.GOAT],
            other_bank=[],
            boat_position=Location.RIGHT_BANK,
            last_item=None
        ),
        State(  # 1
            current_bank=[Item.GOAT, Item.CABBAGE, Item.WOLF],
            other_bank=[],
            boat_position=Location.RIGHT_BANK,
            last_item=Item.WOLF
        ),
        State(  # 2
            current_bank=[Item.WOLF, Item.CABBAGE, Item.GOAT],
            other_bank=[],
            boat_position=Location.LEFT_BANK,
            last_item=None
        ),
        State(  # 3
            current_bank=[Item.GOAT],
            other_bank=[Item.WOLF, Item.CABBAGE],
            boat_position=Location.LEFT_BANK,
            last_item=Item.GOAT
        ),
        State(  # 4
            current_bank=[Item.CABBAGE, Item.WOLF],
            other_bank=[Item.GOAT],
            boat_position=Location.RIGHT_BANK,
            last_item=Item.WOLF
        ),
        State(  # 5
            current_bank=[Item.CABBAGE, Item.WOLF],
            other_bank=[Item.GOAT],
            boat_position=Location.LEFT_BANK,
            last_item=Item.WOLF
        ),
        State(  # 6
            current_bank=[Item.CABBAGE, Item.WOLF],
            other_bank=[],
            boat_position=Location.LEFT_BANK,
            last_item=None
        ),
        State(  # 7
            current_bank=[Item.WOLF],
            other_bank=[Item.GOAT, Item.CABBAGE],
            boat_position=Location.LEFT_BANK,
            last_item=Item.WOLF
        )
    ]

    def test_eq(self):
        self.assertEqual(self.states[0], self.states[1])
        self.assertNotEqual(self.states[0], self.states[2])

    def test_hash(self):
        self.assertEqual(len({self.states[0], self.states[1]}), 1)

    def test_is_over(self):
        self.assertTrue(self.states[1].is_over)
        self.assertTrue(self.states[0].is_over)
        self.assertFalse(self.states[2].is_over)

    def test_is_valid(self):
        self.assertFalse(self.states[6].is_valid)
        self.assertFalse(self.states[7].is_valid)
        self.assertTrue(self.states[0].is_valid)
        self.assertTrue(self.states[1].is_valid)
        self.assertTrue(self.states[2].is_valid)
        self.assertTrue(self.states[3].is_valid)
        self.assertTrue(self.states[4].is_valid)
        self.assertTrue(self.states[5].is_valid)


class TestBankValidator(TestCase):
    banks = [
        [],  # 0
        [Item.GOAT],  # 1
        [Item.WOLF, Item.CABBAGE],  # 2
        [Item.GOAT, Item.WOLF],  # 3
        [Item.WOLF, Item.GOAT]  # 4
    ]

    def test_bank(self):
        self.assertTrue(BankValidator.is_stable(self.banks[0]))
        self.assertTrue(BankValidator.is_stable(self.banks[1]))
        self.assertTrue(BankValidator.is_stable(self.banks[2]))
        self.assertFalse(BankValidator.is_stable(self.banks[3]))
        self.assertFalse(BankValidator.is_stable(self.banks[4]))


class TestNewStateFinder(TestCase):

    def test_empty_move_is_winning(self):
        pass

    def test_get_new_states(self):
        pass


class TestEngine(TestCase):

    def test_initial_state(self):
        engine = Engine()
        self.assertEqual(engine._initial_state, State.initial_state())


class TestUtility(TestCase):

    def test_is_longer_than_one(self):
        self.assertTrue(Utility.is_longer_than_one([1, 2, 3]))
        self.assertFalse(Utility.is_longer_than_one([2]))

    def test_remove_duplicates(self):
        self.assertEqual(Utility.remove_duplicates([1, 1, 2, 3, 3, 4, 5, 5]), {1, 2, 3, 4, 5})

    def test_pluralize(self):
        self.assertEqual(Utility.pluralize('horse', 5), '5 horses')
        self.assertEqual(Utility.pluralize('rock', 2), '2 rocks')
        self.assertEqual(Utility.pluralize('house', 1), '1 house')
        self.assertEqual(Utility.pluralize('car', 0), '0 cars')


if __name__ == '__main__':
    unittest.main()
