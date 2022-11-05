from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp # NOQA

class BaseAppScreen(MDScreen):

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
    