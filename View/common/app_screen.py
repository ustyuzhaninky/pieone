from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp # NOQA
from kivy.factory import Factory
from kivymd.uix.widget import MDWidget

class BaseAppScreen(MDScreen):
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        Factory.unregister('Placeholder')
        Factory.register('Placeholder', cls=self.screen_content)
        super().__init__(**kwargs)
    