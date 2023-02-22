
import os
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.spinner import MDSpinner

from View.screens import screens
from View.MenuScreen.menu_screen import MenuScreenView # NOQA
from View.RegistrationScreen.registration_screen import RegistrationScreenView # NOQA
from View.SchematicScreen.schematic_screen import SchematicScreenView # NOQA
from View.SimulatorScreen.simulator_screen import SimulatorScreenView # NOQA
from View.AboutScreen.about_screen import AboutScreenView # NOQA
from View.DocumentationScreen.documentation_screen import ( # NOQA
    DocumentationScreenView)
from View.common.error_screen import ErrorScreenView
from View.common.tbr_screen import TbrScreenView


class ManagerScreen(MDScreenManager):
    dialog_wait = None
    _screen_names = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.transition = SlideTransition()

    def create_screen(self, name_screen):
        if name_screen not in self._screen_names:
            self._screen_names.append(name_screen)
            self.load_common_package()
            view = TbrScreenView()
            view.name = name_screen
            if name_screen not in screens.keys():
                return view
            try:
                exec(f"import View.{screens[name_screen]}")
                self.app.load_all_kv_files(
                    os.path.join(self.app.directory,
                                 "View",
                                 screens[name_screen].split(".")[0])
                )
                view = eval(
                    f'View.{screens[name_screen]}'
                    f'.{screens[name_screen].split(".")[0]}View()'
                )
                view.name = name_screen
            except Exception:
                view = ErrorScreenView()
                view.name = name_screen
            return view

    def load_common_package(self) -> None:
        def _load_kv(common_path):
            for it in sorted(os.listdir(common_path)):
                if os.path.isfile(
                        os.path.join(common_path, it)):
                    kv_loaded = False
                    for loaded_path_kv in Builder.files:
                        if os.path.join(common_path, it) in loaded_path_kv:
                            kv_loaded = True
                            break
                    if not kv_loaded:
                        if os.path.join(
                           common_path, it).lower().endswith(".kv"):
                            self.app.load_kv(os.path.join(common_path, it))
                else:
                    _load_kv(os.path.join(common_path, it))
        _load_kv(os.path.join(os.environ["PIEONE_ROOT"], "View", "common"))

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
            self.dialog_wait = ModalView(background_color=[0, 0, 0, 0])
            self.dialog_wait.add_widget(spinner)
        self.dialog_wait.open()
        Clock.schedule_once(self.dialog_wait.dismiss, 1.5)

    def add_screen(self, view) -> None:
        self.add_widget(view)
