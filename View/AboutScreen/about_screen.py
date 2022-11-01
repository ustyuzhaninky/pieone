import os

from kivymd.uix.screen import MDScreen
from View import TopBar # NOQA
from View import BottomBar # NOQA

class AboutScreenView(MDScreen):
    def on_enter(self) -> None:
        if not self.ids.about_label.text:
            with open(
                f"{os.environ['PIEONE_ROOT']}/assets/data/about_screen/about.txt",
                encoding="utf-8",
            ) as about:
                self.ids.about_label.text = about.read()