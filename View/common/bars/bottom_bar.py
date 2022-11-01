import os
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.widget import MDWidget
from kivymd.app import MDApp
from kivy.core.window import Window

class BottomBar(MDTopAppBar):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.on_action_button = lambda x: self.return_callback(x)
        self.icon = "arrow-left"
        self.mode = "end"
    
    def menu_callback(self):
        pass
    
    def return_callback(self, widget):
        self.app.manager_screen.current = "menu"
        return self.app.manager_screen.current