from kivy.properties import StringProperty, ObjectProperty

from View.common.rectangular_card import RectangularCard
from kivymd.app import MDApp # NOQA

class MenuCard(RectangularCard):
    title = StringProperty()
    source = StringProperty()
    action = ObjectProperty()

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
        
