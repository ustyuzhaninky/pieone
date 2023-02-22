from kivymd.app import MDApp # NOQA
from kivymd.uix.boxlayout import MDBoxLayout
from View.common.app_screen import BaseAppScreen


class TbrContent(MDBoxLayout):

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)


class TbrScreenView(BaseAppScreen):
    screen_content = TbrContent
    noreturn = False

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)