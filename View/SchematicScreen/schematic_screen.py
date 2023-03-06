import os

from kivy.resources import resource_find
from View.common.app_screen import BaseAppScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp


class SchematicContent(MDBoxLayout):
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)

    def get_text(self, slide_index) -> str:
        with open(
                resource_find(
                    f"{os.environ['PIEONE_ROOT']}/assets"
                    f"/data/schematic_screen/sc{slide_index+1}_desc.txt"),
                "rt",
                encoding="utf-8") as screen_label_text:
            return screen_label_text.read()

    def set_stage_image(self, stage, *args):
        self.ids.image.source = resource_find(
            f"{os.environ['PIEONE_ROOT']}\\assets\\"
            f"images\\schematic_screen\\mnemo_st{stage}.png")
        self.ids.image.reload()


class SchematicScreenView(BaseAppScreen):
    screen_content = SchematicContent

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
