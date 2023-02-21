from kivymd.app import MDApp # NOQA
from kivymd.uix.boxlayout import MDBoxLayout
from View.common.app_screen import BaseAppScreen
from kivy.properties import StringProperty

class ErrorContent(MDBoxLayout):

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)

class ErrorScreenView(BaseAppScreen):
    screen_content = ErrorContent
    noreturn = False

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)