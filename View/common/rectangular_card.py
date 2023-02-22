from kivymd.uix.card import MDCard
from kivymd.app import MDApp # NOQA


class RectangularCard(MDCard):
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
