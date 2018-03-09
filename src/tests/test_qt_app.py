import unittest
from mock import Mock, patch
from player.qt_app import App, SETTINGS
from player.player import MediaPlayer

class TestApp(unittest.TestCase):

    def setUp(self):
        app = App()
        app.build()
        self.app = app

    @patch('player.simple.Service')
    def test_autoplay(self, Service):
        player = Mock()
        Service.get_player = Mock(return_value=player)

        mp = MediaPlayer({'autoplay': False}, build=False)
        player.play.assert_not_called()

        # mp = MediaPlayer({'autoplay': False}, build=False)
        # player.play.assert_called_with()


    #@patch('player.media.QPixmap')
    def test_config_set_frame(self):
        '''Changing the frameless conf calls and changes flags'''
        app = self.app

        icon = app.app.windowIcon()
        self.assertTrue(icon.isNull())

        pixmap = app.set_app_icon(SETTINGS)
        icon = app.app.windowIcon()
        self.assertFalse(icon.isNull())
        #app.app.setWindowIcon.assertCalled()

    @patch('sys.exit')
    def test_run(self, _exit):
        lambda_ret = Mock()
        app = App()
        app.app = Mock
        app.app.exec_ = lambda: lambda_ret
        app.config = {}
        app.build = Mock()
        app.set_app_icon = Mock()

        app.run()

        app.set_app_icon.assert_called_with(app.config)
        app.build.assert_called()
        _exit.assert_called_with(lambda_ret)



