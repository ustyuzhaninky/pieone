import os
from kivy.factory import Factory
from kivy.properties import BooleanProperty, ListProperty
from kivy.resources import resource_find
from kivymd.uix.widget import MDWidget
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp # NOQA

class BaseAppScreen(MDScreen):
    noreturn = BooleanProperty(False)
    returntool = ListProperty([])

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        Factory.unregister('Placeholder')
        Factory.register('Placeholder', cls=self.screen_content)
        super().__init__(**kwargs)
    
    def get_left_button(self) -> list:
        if self.noreturn:
            return [
                resource_find(f"{os.environ['PIEONE_ASSETS']}/images/pieone-logo.png"),
                self.no_return_action,
                "P.I.E. ONE",
                "P.I.E. ONE"]
        else:
            return self.returntool
    
    def no_return_action(self, widget) -> None:
        pass