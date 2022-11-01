from kivy.properties import StringProperty

from View.common.rectangular_card import RectangularCard
from kivymd.app import MDApp # NOQA

class MenuCard(RectangularCard):
    title = StringProperty()
    source = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
