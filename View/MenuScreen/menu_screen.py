import os

from View.common.app_screen import BaseAppScreen
from kivymd.app import MDApp # NOQA
from View.MenuScreen.components import MenuCard  # NOQA
from kivymd.uix.boxlayout import MDBoxLayout

class MenuContent(MDBoxLayout):
    
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
        self.app.bind(darkmode=self.swap_images)

    def swap_images(self, instance, darkmode):
        if darkmode==True:
            self.ids.simulator_card.source = self.app.asset(
                f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/simulator-dark.png")
            self.ids.schematic_card.source = self.app.asset(
                f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/schematic-dark.png")
            self.ids.documentation_card.source = self.app.asset(
                f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/documentation-dark.png")
            self.ids.about_card.source = self.app.asset(
                f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/about-dark.png")
        else:
            self.ids.simulator_card.source = self.app.asset(
                f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/simulator.png")
            self.ids.schematic_card.source = self.app.asset(
                f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/schematic.png")
            self.ids.documentation_card.source = self.app.asset(
                f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/documentation.png")
            self.ids.about_card.source = self.app.asset(
                f"{os.environ['PIEONE_ASSETS']}/images/menu_screen/about.png")

class MenuScreenView(BaseAppScreen):
    screen_content = MenuContent
    noreturn = True

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
