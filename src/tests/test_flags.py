import unittest
from player.flags import FlagsMixin
from mock import Mock


class TestFlags(unittest.TestCase):

    def test_add_flags(self):
        fl = FlagsMixin()

        self.assertEqual(fl.flags, None)

        fl.add_flag('Cake')
        fl.add_flag('Apples')
        fl.add_flag('Apples')

        self.assertEqual(len(fl.flags), 2)

    def test_set_flags(self):

        fl = FlagsMixin()
        fl.flags = [1,2,3,4,5]
        fl.setWindowFlag = Mock()

        fl.set_flags()

        cc = fl.setWindowFlag.call_count
        # A tick per flag
        self.assertEqual(cc, 5)

        # Iter each call, noting the flag was called correctly
        counter = 0
        for call_ in fl.setWindowFlag.call_args_list:
            counter += 1
            self.assertTupleEqual((counter, True), call_[0])
