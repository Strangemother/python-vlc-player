import unittest
from player.player import ConfigMixin


class TestMediaPlayer(unittest.TestCase):

    def test_config_set_frame(self):
        '''Changing the frameless conf calls and changes flags'''
        pl = ConfigMixin()
        pl.settings = { 'frameless': True }

        return_value = pl.config_set_frame()

        self.assertTrue(return_value, True)
        self.assertEqual(len(pl.flags), 1)

        return_value = pl.config_set_frame(value=False)
        self.assertEqual(len(pl.flags), 0)

        pl.config_set_frame(value=True)
        pl.config_set_frame(value=True)

        self.assertEqual(len(pl.flags), 1)


