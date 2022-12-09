import os

from View.common.app_screen import BaseAppScreen
from kivy.resources import resource_add_path, resource_find

class AboutScreenView(BaseAppScreen):
    def on_enter(self) -> None:
        if not self.ids.about_label.text:
            with open(
                resource_find(f"{os.environ['PIEONE_ROOT']}/assets/data/about_screen/about.txt"),
                encoding="utf-8",
            ) as about:
                self.ids.about_label.text = about.read()