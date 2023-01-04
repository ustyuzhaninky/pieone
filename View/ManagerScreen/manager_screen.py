
import os

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import NoTransition, SlideTransition
from kivy.utils import get_color_from_hex
from kivy.resources import resource_add_path, resource_find
from kivymd.app import MDApp
from kivymd.utils.set_bars_colors import set_bars_colors
from kivymd.color_definitions import colors
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.spinner import MDSpinner

from View.screens import screens
from View.MenuScreen.menu_screen import MenuScreenView
from View.RegistrationScreen.registration_screen import RegistrationScreenView
from View.SchematicScreen.schematic_screen import SchematicScreenView
from View.SimulatorScreen.simulator_screen import SimulatorScreenView
from View.AboutScreen.about_screen import AboutScreenView
from View.DocumentationScreen.documentation_screen import DocumentationScreenView


class ManagerScreen(MDScreenManager):
    dialog_wait = None
    _screen_names = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.transition = SlideTransition()

    def on_current(self, *args):
        super().on_current(*args)
        self.set_bars_colors(self.app.theme_cls, self.current)

    def set_bars_colors(self, instance_theme_cls, name_screen: str) -> None:
        primary_color = instance_theme_cls.primary_color
        bg_normal = instance_theme_cls.bg_normal

        panel_colors = {
            "menu": {
                "status_bar_color": primary_color,
                "navigation_bar_color": bg_normal,
                "navigation_icon_color": "Light",
            },
            "simulator": {
                "status_bar_color": primary_color,
                "navigation_bar_color": bg_normal,
                "navigation_icon_color": "Light",
            },
            "schematic": {
                "status_bar_color": primary_color,
                "navigation_bar_color": bg_normal,
                "navigation_icon_color": "Light",
            },
            "documentation": {
                "status_bar_color": primary_color,
                "navigation_bar_color": bg_normal,
                "navigation_icon_color": "Light",
            },
            "about": {
                "status_bar_color": primary_color,
                "navigation_bar_color": bg_normal,
                "navigation_icon_color": "Light",
            },
        }

        if name_screen in panel_colors:
            set_bars_colors(
                panel_colors[name_screen]["status_bar_color"],
                panel_colors[name_screen]["navigation_bar_color"],
                panel_colors[name_screen]["navigation_icon_color"],
            )

    def create_screen(self, name_screen):
        if name_screen not in self._screen_names:
            self._screen_names.append(name_screen)
            self.load_common_package(name_screen)
            exec(f"import View.{screens[name_screen]}")
            self.app.load_all_kv_files(
                os.path.join(self.app.directory, "View", screens[name_screen].split(".")[0])
            )
            view = eval(
                f'View.{screens[name_screen]}.{screens[name_screen].split(".")[0]}View()'
            )
            view.name = name_screen
            return view

    def load_common_package(self, name_screen) -> None:
        def _load_kv(path_to_kv):
            kv_loaded = False
            for loaded_path_kv in Builder.files:
                if path_to_kv in loaded_path_kv:
                    kv_loaded = True
                    break
            if not kv_loaded:
                if name_screen in ["list"]:
                    from kivy.factory import Factory

                    Factory.register(
                        "OneLineItem",
                        module="View.common.onelinelistitem.one_line_list_item",
                    )
                Builder.load_file(path_to_kv)

        one_line_list_item_path = os.path.join(
            "View", "common", "onelinelistitem", "one_line_list_item.kv"
        )
        dots_path = os.path.join("View", "common", "dots", "dots.kv")

        if name_screen in ["list"]:
            _load_kv(one_line_list_item_path)
        elif name_screen in ["button", "field"]:
            _load_kv(dots_path)

    def switch_screen(self, screen_name: str) -> None:
        def switch_screen(*args):
            if screen_name not in self._screen_names:
                self.open_dialog()
                screen = self.create_screen(screen_name)
                self.add_screen(screen)
            if self.current == "menu":
                self.transition.direction = 'right'
            else:
                self.transition.direction = 'left'
            self.current = screen_name
        Clock.schedule_once(switch_screen)

    def open_dialog(self) -> None:
        if not self.dialog_wait:
            spinner = MDSpinner(
                size=(75, 75),
                size_hint=(None, None),
                pos_hint={'center_x': .5, 'center_y': .5},
                active=True,
            )
            self.dialog_wait = ModalView()
            self.dialog_wait.add_widget(spinner)
        self.dialog_wait.open()
        Clock.schedule_once(self.dialog_wait.dismiss, 1.5)

    def add_screen(self, view) -> None:
        self.add_widget(view)
