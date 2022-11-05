import os

from View.common.app_screen import BaseAppScreen
from kivymd.app import MDApp # NOQA
from View.MenuScreen.components import MenuCard  # NOQA
from kivymd.uix.screen import MDScreen

class MenuScreenView(BaseAppScreen):
    
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
    
    def on_enter(self, *args) -> None:
        self.ids.simulator_card.on_release = lambda: self.manager.switch_screen('simulator')
        self.ids.schematic_card.on_release = lambda: self.manager.switch_screen('schematic')
        self.ids.documentation_card.on_release = lambda: self.manager.switch_screen('documentation')
        self.ids.about_card.on_release = lambda: self.manager.switch_screen('about')
        self.swap_images(self, self.app.darkmode)

        self.app.bind(darkmode=self.swap_images)
    
    def swap_images(self, instance, darkmode):
        if darkmode==True:
            self.ids.simulator_card.source = f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/simulator-dark.png"
            self.ids.schematic_card.source = f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/schematic-dark.png"
            self.ids.documentation_card.source = f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/documentation-dark.png"
            self.ids.about_card.source = f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/about-dark.png"
        else:
            self.ids.simulator_card.source = f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/simulator.png"
            self.ids.schematic_card.source = f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/schematic.png"
            self.ids.documentation_card.source = f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/documentation.png"
            self.ids.about_card.source = f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/about.png"
