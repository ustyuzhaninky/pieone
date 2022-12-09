import os

from kivy.resources import resource_add_path, resource_find
from View.common.app_screen import BaseAppScreen
from kivymd.app import MDApp

class SchematicScreenView(BaseAppScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

        self.set_stage_image(0)

    def on_enter(self) -> None:
        labels = [
            self.ids.screen_1_label,
            self.ids.screen_2_label,
            self.ids.screen_3_label,
            self.ids.screen_4_label,
            self.ids.screen_5_label,
            self.ids.screen_6_label,
            self.ids.screen_7_label,
        ]
        for i, label in enumerate(labels):
            if not label.text:
                with open(
                    resource_find(f"{os.environ['PIEONE_ROOT']}/assets/data/schematic_screen/sc{i+1}_desc.txt"),
                    "rt",
                    encoding="utf-8") as screen_label_text:
                    labels[i].text = screen_label_text.read()
        
    def set_stage_image(self, stage, *args):
        self.ids.image.source = resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\schematic_screen\\mnemo_st{stage}.png")
        self.ids.image.reload()
