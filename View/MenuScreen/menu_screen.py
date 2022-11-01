import os

from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp # NOQA
from View.MenuScreen.components import MenuCard  # NOQA
from View import TopBar # NOQA
from View import BottomBar # NOQA

class MenuScreenView(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def on_enter(self, *args) -> None:
        if not self.ids.menu_list.data:
            menu_list = [
                "simulator",
                "schematic",
                "documentation",
                "about",
            ]
            menu_names = [
                self.app.tr._("Simulator"),
                self.app.tr._("Schematic"),
                self.app.tr._("Documentation"),
                self.app.tr._("About"),
            ]
            # menu_list.sort()
            for idx, name_card in enumerate(menu_list):
                if not self.app.darkmode:
                    source = f"images/menu_screen/{name_card.lower()}.png"
                else:
                    source = f"images/menu_screen/{name_card.lower()}-dark.png"
                self.ids.menu_list.data.append(
                    {
                        "viewclass": "MenuCard",
                        "title": menu_names[idx],
                        # "elevation": 3,
                        "on_release": lambda x=name_card.lower(): self.manager.switch_screen(
                            x
                        ),
                        "source": (
                            f"{os.environ['PIEONE_ASSETS']}/{source}"
                        ),
                        "app": self.app,
                    }
                )
