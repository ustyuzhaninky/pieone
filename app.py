# coding=utf-8
# Copyright (c) 2022, Konstantin Usiuzhanin

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# @author: Konstantin Ustyuzhanin

import gettext
import os
import sys
from dataclasses import dataclass
from pathlib import Path

os.environ["KIVY_GL_BACKEND"] = "sdl2"
import kivy

kivy.require('2.1.0')
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Observable
from kivy.metrics import dp
from kivy.properties import (BooleanProperty, ConfigParser,
                             ConfigParserProperty, ListProperty,
                             ObjectProperty)
from kivy.resources import resource_add_path, resource_find
from kivy.uix.settings import Settings
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.snackbar import Snackbar

from View.ManagerScreen.manager_screen import ManagerScreen

if getattr(sys, "frozen", False) and hasattr(sys, '_MEIPASS'):
    os.environ["PIEONE_ROOT"] = sys._MEIPASS
else:
    sys.path.append(os.path.abspath(__file__).split("demos")[0])
    os.environ["PIEONE_ROOT"] = str(Path(__file__).parent)
os.environ["PIEONE_ASSETS"] = os.path.join(
    os.environ["PIEONE_ROOT"], f"assets{os.sep}"
)
Window.softinput_mode = "below_target"
# Window.borderless = True


@dataclass
class TestData:
    events_solved = None
    total_time = None
    mean_time = None
    accuracy = None
    confidence = None

    def __init__(
        self,
        events_solved,
        total_time,
        mean_time,
        accuracy,
        confidence
    ) -> None:
        self.events_solved = events_solved
        self.total_time = total_time
        self.mean_time = mean_time
        self.accuracy = accuracy
        self.confidence = confidence


class Lang(Observable):
    observers = []
    lang = None

    def __init__(self, defaultlang):
        super(Lang, self).__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        return self.ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super(Lang, self).fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super(Lang, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = resource_find(
            os.path.join(os.environ["PIEONE_ROOT"], 'assets', 'locales'))
        locales = gettext.translation('pieone', locale_dir, languages=[lang])
        self.ugettext = locales.gettext
        self.lang = lang

        # update all the kv rules attached to this text
        for func, largs, kwargs in self.observers:
            func(largs, None, None)


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.ids.check.on_release = kwargs['on_release']

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


class YesAndStopButton(MDFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.on_release = lambda: self.app.stop()


class NoAndKeepButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.on_release = lambda: self.app.close_application_dialog.dismiss()


class CloseApplicationDialog(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()


class RestartLaterButton(MDFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.on_release = lambda: self.app.restart_dialog.dismiss()


class RestartNowButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.on_release = lambda: self.app.stop()


class RestartDialog(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()


class OkLanguageDialogButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()


class LanguageDialog(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()


class YesLeaveSimulationDialogButton(MDFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()


class CloseLeaveSimulationDialogButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.on_release = lambda: self.app.leave_simulation_dialog.dismiss()


class LeaveSimulationDialog(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()


class SimulatorApp(MDApp):

    # Multi-session savables
    darkmode = ConfigParserProperty(
        True,
        'Graphics', 'darkmode',
        'simulator',
        val_type=bool,
        errorvalue=False)
    locale = ConfigParserProperty(
        'ru',
        'System', 'locale',
        'simulator',
        val_type=str,
        errorvalue='en',
        verify=lambda x: True if (
            isinstance(x, str)) and (
                x in ['en', 'ru']) else False)

    # One-session properties and objects
    unsaved_progress = BooleanProperty(False)
    user_data = ObjectProperty()

    # UI suppliments
    close_dialog_buttons = ListProperty([])
    restart_dialog_buttons = ListProperty([])
    language_dialog_buttons = ListProperty([])
    leave_simulation_dialog_buttons = ListProperty([])
    language_items = ListProperty([])
    leave_simulation_dialog = ObjectProperty()
    settings_dialog = ObjectProperty()
    language_dialog = ObjectProperty()
    restart_dialog = ObjectProperty()
    close_application_dialog = ObjectProperty()
    tr = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tr = Lang("en")
        self.tr.switch_lang(self.locale)
        self.icon = resource_find(
            f"{os.environ['PIEONE_ROOT']}/assets/images/pieone-logo.png")
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Indigo"
        self.snackbar = None
        self._interval = 0
        self.manager_screen = ManagerScreen()

    def build(self) -> ManagerScreen:
        """
        Build and return the root widget.
        """

        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.1
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.width = Window.width
        self.height = Window.height
        self.settings_cls = Settings
        # self.settings_cls = MDSettingsWithExpansionPanels
        self.use_kivy_settings = False

        self.load_kv(os.path.join(self.directory, "app.kv"))
        self.manager_screen.add_screen(
            self.manager_screen.create_screen("menu"))
        # Window.custom_titlebar = True
        # Window.set_custom_titlebar(TopBar())
        Window.set_icon(resource_find(
            f"{os.environ['PIEONE_ROOT']}/assets/images/pieone-logo.png"))
        Window.maximize()

        self.config = ConfigParser(name='simulator')
        if not os.path.exists(f"{os.environ['PIEONE_ROOT']}/simulator.ini"):
            self.config = self.build_config(
                self.config
            )
            self.config.read(
                f"{os.environ['PIEONE_ROOT']}/configs/default.ini"
            )
            self.config.read(
                f"{os.environ['PIEONE_ROOT']}/simulator.ini"
            )
        else:
            self.config.read(
                f"{os.environ['PIEONE_ROOT']}/simulator.ini")
        self._restore_app_state()

        return self.manager_screen

    def set_user_data(self, data: dict):
        self.user_data = TestData(
            events_solved=data['events_solved'],
            total_time=data['total_time'],
            mean_time=data['mean_time'],
            accuracy=data['accuracy'],
            confidence=data['confidence']
        )

    def stop_callback(self):
        self.close_dialog_buttons = [YesAndStopButton(), NoAndKeepButton()]
        self.close_application_dialog = CloseApplicationDialog()
        self.close_application_dialog.open()

    def display_settings(self, settings):
        if not self.settings_dialog:
            button_ok = MDFlatButton(
                text=self.tr._("Ok"),
                text_color=self.theme_cls.primary_color,
            )
            button_apply = MDFlatButton(
                text=self.tr._("Cancel"),
                disabled='True',
                text_color=self.theme_cls.primary_color,
            )
            button_cancel = MDRaisedButton(
                text=self.tr._("Cancel"),
            )
            self.settings_dialog = MDDialog(
                title=self.tr._('Settings'),
                type="custom",
                content_cls=MDBoxLayout(
                    settings,
                    size_hint_y=None,
                    orientation="vertical",
                    height="620dp",),
                size_hint=(0.8, 0.8),
                buttons=[
                    button_ok,
                    button_apply,
                    button_cancel,
                ],
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                height=Window.height + dp(10),
            )

            def ok_callback(*args):
                self.close_settings()

            def apply_callback(*args):
                self.close_settings()

            def cancel_callback(*args):
                self.close_settings()

            button_ok.on_release = ok_callback
            button_apply.on_release = apply_callback
            button_cancel.on_release = cancel_callback
        dg = self.settings_dialog
        if dg.content_cls is not settings:
            dg.content_cls = settings
        dg.open()

    def _restore_app_state(self):
        self.darkmode = self.config.getboolean('Graphics', 'darkmode')
        self.locale = self.config.get('System', 'locale')
        self.config.write()

        if self.darkmode:
            self.theme_cls.primary_palette = "Orange"
            self.theme_cls.theme_style = "Dark"
            self.darkmode = True
        else:
            self.theme_cls.primary_palette = "Blue"
            self.theme_cls.theme_style = "Light"
            self.darkmode = False
        self.tr.switch_lang(self.locale)

    def switch_theme_style(self):
        if self.darkmode:
            self.theme_cls.primary_palette = "Blue"
            self.theme_cls.theme_style = "Light"
            self.darkmode = False
        else:
            self.theme_cls.primary_palette = "Orange"
            self.theme_cls.theme_style = "Dark"
            self.darkmode = True
        self.config.set('Graphics', 'darkmode', self.darkmode)

    def open_restart_dialog(self):
        if not self.restart_dialog:
            self.restart_dialog_buttons = [
                RestartLaterButton(),
                RestartNowButton()
            ]
            self.restart_dialog = RestartDialog()
        self.restart_dialog.open()

    def open_language_dialog(self):
        if not self.language_dialog:
            ok_button = OkLanguageDialogButton()

            def ok_callback(*args):
                self.language_dialog.dismiss()
                self.open_restart_dialog()

            ok_button.on_release = ok_callback
            self.language_dialog_buttons = [ok_button]

            def set_language(lang):
                self.locale = lang
                self.tr.switch_lang(self.locale)

            self.language_items = [
                ItemConfirm(
                    text="English (USA)",
                    on_release=lambda x=None: set_language("en")
                ),
                ItemConfirm(
                    text="Русский (Россия)",
                    on_release=lambda x=None: set_language("ru")
                ),
            ]
            self.language_dialog = LanguageDialog(
                items=self.language_items
            )
        self.language_dialog.open()

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('System', {'locale': 'en'})
        config.setdefaults('Graphics', {'darkmode': False})

        return config

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        settings.add_json_panel(
            'System',
            self.config,
            filename=os.path.join(
                os.environ['PIEONE_ROOT'], "configs", "graphics.json"))
        settings.add_json_panel(
            'Graphics',
            self.config,
            filename=os.path.join(
                os.environ['PIEONE_ROOT'], "configs", "system.json"))
        return settings

    def on_stop(self):
        self.config.set('Graphics', 'darkmode', self.darkmode)
        self.config.set('System', 'locale', self.locale)
        self.config.write()

    def wait_interval(self, interval):
        self._interval += interval
        if self._interval > self.snackbar.duration + 0.5:
            anim = Animation(y=dp(10), d=.2)
            anim.start(self.screen.ids.button)
            Clock.unschedule(self.wait_interval)
            self._interval = 0
            self.snackbar = None

    def on_settings_callback(self, sender):
        if not self.settings_panel.disabled:
            self.manager_screen.switch_screen("settings")

    def log_callback(self, button, text):
        if not self.snackbar:
            self.snackbar = Snackbar(
                text=text,
                snackbar_x="10dp",
                snackbar_y="10dp",
            )
            self.snackbar.size_hint_x = (
                Window.width - (self.snackbar.snackbar_x * 2)
            ) / Window.width
            self.snackbar.buttons = [
                MDFlatButton(
                    text="CANCEL",
                    text_color=(1, 1, 1, 1),
                    on_release=self.snackbar.dismiss,
                ),
            ]
        self.snackbar.open()

    def return_callback(self, widget, return_to='menu'):
        if self.unsaved_progress:
            if not self.leave_simulation_dialog:
                yes_button = YesLeaveSimulationDialogButton()
                self.leave_simulation_dialog_buttons = [
                    yes_button,
                    CloseLeaveSimulationDialogButton()
                ]
                self.leave_simulation_dialog = LeaveSimulationDialog()

                def yes_callback(*args):
                    self.leave_simulation_dialog.dismiss()
                    self.unsaved_progress = False
                    self.manager_screen.switch_screen(return_to)
                yes_button.on_release = yes_callback
            self.leave_simulation_dialog.open()

            return self.manager_screen.current
        else:
            self.manager_screen.switch_screen(return_to)
            return self.manager_screen.current

    def maximize_callback(self):
        if self.is_maximized == self.is_maximized:
            self.is_maximized = not self.is_maximized
            Window.maximize()
        else:
            Window.restore()

    def menu_callback(self):
        pass

    def asset(self, asset_path: str) -> str:
        if resource_find(asset_path):
            return resource_find(asset_path)
        else:
            return resource_find(
                f"{os.environ['PIEONE_ASSETS']}/images/image-broken.png"
            )


def main(*args, **kwargs):
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    resource_add_path(os.environ["PIEONE_ROOT"])
    SimulatorApp().run()


if __name__ == '__main__':
    main()
