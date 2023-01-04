import os

from kivymd.app import MDApp # NOQA
from kivymd.uix.boxlayout import MDBoxLayout
from View.common.app_screen import BaseAppScreen
from kivy.resources import resource_add_path, resource_find

class AboutContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get_about_text(self, *args):
        if not self.ids.about_label.text:
            with open(
                resource_find(f"{os.environ['PIEONE_ROOT']}/assets/data/about_screen/about.txt"),
                encoding="utf-8",
            ) as about:
                text = about.read()
        return text

class AboutScreenView(BaseAppScreen):
    screen_content = AboutContent

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
