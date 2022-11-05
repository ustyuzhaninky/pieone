"""

Copyright (c) 2022, Konstantin Usiuzhanin

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

@author: Konstantin Ustyuzhanin

"""

import sys
import os
import gettext
from pathlib import Path
from random import random
from functools import partial
os.environ["KIVY_GL_BACKEND"]= "angle_sdl2"
import kivy
kivy.require('2.1.0')

from random import randint
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import (
    ConfigParserProperty, ConfigParser, OptionProperty,
    StringProperty, ObjectProperty, NumericProperty,
    BooleanProperty, ListProperty)
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.config import Config
from kivy.uix.settings import Settings
from kivy.logger import Logger
from kivy.lang import Observable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.button import (
    MDFlatButton, MDRaisedButton)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton

from View.ManagerScreen.manager_screen import ManagerScreen
from View.SettingsScreen.settings_screen import MDSettingsWithExpansionPanels

if getattr(sys, "frozen", False):
    os.environ["PIEONE_ROOT"] = sys._MEIPASS
else:
    sys.path.append(os.path.abspath(__file__).split("demos")[0])
    os.environ["PIEONE_ROOT"] = str(Path(__file__).parent)
os.environ["PIEONE_ASSETS"] = os.path.join(
    os.environ["PIEONE_ROOT"], f"assets{os.sep}"
)
Window.softinput_mode = "below_target"
# Window.borderless = True

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
        locale_dir = os.path.join(os.environ["PIEONE_ROOT"], 'assets', 'locales')
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
        self.ids.check.on_release =  kwargs['on_release']

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
        False,
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
        verify=lambda x: True if (isinstance(x, str)) and (x in ['en', 'ru']) else False)

    # One-session properties and objects
    unsaved_progress = BooleanProperty(False)
        
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
        self.icon = f"{os.environ['PIEONE_ROOT']}/assets/images/pieone-logo.png"
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
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.accent_palette = "Yellow"
        self.width = Window.width
        self.height = Window.height
        self.settings_cls = Settings
        # self.settings_cls = MDSettingsWithExpansionPanels
        self.use_kivy_settings = False

        self.load_kv(os.path.join(self.directory, "app.kv"))
        self.manager_screen.add_widget(self.manager_screen.create_screen("menu"))
        # Window.custom_titlebar = True
        # Window.set_custom_titlebar(TopBar())
        Window.set_icon(f"{os.environ['PIEONE_ROOT']}/assets/images/pieone-logo.png")
        Window.maximize()

        self.config = ConfigParser(name='simulator')
        if not os.path.exists(
            f"{os.environ['PIEONE_ROOT']}/simulator.ini"):
            self.config = self.build_config(
                self.config)
            self.config.read(
                f"{os.environ['PIEONE_ROOT']}/configs/default.ini")
            self.config.read(
                f"{os.environ['PIEONE_ROOT']}/simulator.ini")
        else:
            self.config.read(
                f"{os.environ['PIEONE_ROOT']}/simulator.ini")

        self._restore_app_state()
        
        return self.manager_screen
    
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
            button_cancel= MDRaisedButton(
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
            button_ok.on_release=ok_callback
            button_apply.on_release=apply_callback
            button_cancel.on_release=cancel_callback
        dg = self.settings_dialog
        if dg.content_cls is not settings:
            dg.content_cls = settings
        dg.open()

    def close_settings(self, *args):
        try:
            dg = self.settings_dialog
            dg.dismiss()
        except AttributeError:
            pass # Settings popup doesn't exist
    
    def _restore_app_state(self):
        self.darkmode = self.config.get('Graphics', 'darkmode')
        self.locale = self.config.get('System', 'locale')

        if self.darkmode==True:
            self.theme_cls.primary_palette = "Orange"
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.accent_palette = "Yellow"
        self.tr.switch_lang(self.locale)

    def set_theme_style(self, darkmode):
        if darkmode:
             self.theme_cls.primary_palette = "Orange"
             self.theme_cls.theme_style = "Dark"
             self.theme_cls.accent_palette = "Yellow"
        else:
            self.theme_cls.primary_palette = "Blue"
            self.theme_cls.theme_style = "Light"
            self.theme_cls.accent_palette = "LightBlue"

    def switch_theme_style(self):
        if self.darkmode==True:
            self.theme_cls.primary_palette = "Blue"
            self.theme_cls.theme_style = "Light"
            self.theme_cls.accent_palette = "LightBlue"
            self.darkmode = False
        else:
            self.theme_cls.primary_palette = "Orange"
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.accent_palette = "Yellow"
            self.darkmode = True
        self.config.set('Graphics', 'darkmode', self.darkmode)
    
    def open_restart_dialog(self):
        if not self.restart_dialog:
            self.restart_dialog_buttons = [RestartLaterButton(), RestartNowButton()]
            self.restart_dialog = RestartDialog()
        self.restart_dialog.open()
    
    def open_language_dialog(self):
        if not self.language_dialog:
            ok_button = OkLanguageDialogButton()
            def ok_callback(*args):
                self.language_dialog.dismiss()
                self.open_restart_dialog()
            ok_button.on_release=ok_callback
            self.language_dialog_buttons = [ok_button]
            def set_language(lang):
                self.locale = lang
                self.tr.switch_lang(self.locale)
            self.language_items = [
                ItemConfirm(text="English (USA)", on_release=lambda x=None: set_language("en")),
                ItemConfirm(text="Русский (Россия)", on_release=lambda x=None: set_language("ru")),
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
            filename=os.path.join(os.environ['PIEONE_ROOT'], "configs", "graphics.json"))
        settings.add_json_panel(
            'Graphics',
            self.config,
            filename=os.path.join(os.environ['PIEONE_ROOT'], "configs", "system.json"))
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

    def return_callback(self, widget):
        if self.unsaved_progress == True:
            if not self.leave_simulation_dialog:
                yes_button = YesLeaveSimulationDialogButton()
                self.leave_simulation_dialog_buttons = [
                    yes_button,
                    CloseLeaveSimulationDialogButton()
                ]
                self.leave_simulation_dialog = LeaveSimulationDialog()
                
                def yes_callback(*args):
                    self.leave_simulation_dialog.dismiss()
                yes_button.on_release = yes_callback
            
            self.leave_simulation_dialog.open()
            self.manager_screen.switch_screen("menu")
            return self.manager_screen.current
        else:
            self.manager_screen.switch_screen("menu")
            return self.manager_screen.current

    def maximize_callback(self):
        if self.is_maximized == self.is_maximized:
            self.is_maximized = not self.is_maximized
            Window.maximize()
        else:
            Window.restore()

    def menu_callback(self):
        pass

def main(*args, **kwargs):
    SimulatorApp().run()

if __name__ == '__main__':
    main()
