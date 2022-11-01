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
os.environ["KIVY_GL_BACKEND"]= "angle_sdl2"
import kivy
kivy.require('2.1.0')

from random import randint
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import (
    ConfigParserProperty, ConfigParser, OptionProperty,
    StringProperty, ObjectProperty, NumericProperty,
    BooleanProperty)
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

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False

class SimulatorApp(MDApp):

    # darkmode = BooleanProperty(True)
    darkmode = ConfigParserProperty(
        True, 'Graphics', 'darkmode',
        'simulator', val_type=bool, errorvalue=False)
    # locale = OptionProperty('ru', options=['en', 'ru'])
    locale = ConfigParserProperty(
        'ru', 'System', 'locale',
        'simulator',
        val_type=str,
        errorvalue='en',
        verify=lambda x: True if (isinstance(x, str)) and (x in ['en', 'ru']) else False)

    unsaved_progress = BooleanProperty(False)
    settings_dialog = ObjectProperty()
    language_dialog = ObjectProperty()
    restart_dialog = ObjectProperty()
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
        self.load_all_kv_files(
                os.path.join(self.directory, "View", "common", "bars", "top_bar.kv")
            )
        self.load_all_kv_files(
                os.path.join(self.directory, "View", "common", "bars", "bottom_bar.kv")
            )
        self.manager_screen.add_widget(self.manager_screen.create_screen("menu"))
        # Window.custom_titlebar = True
        # Window.set_custom_titlebar(TopBar())
        Window.set_icon(f"{os.environ['PIEONE_ROOT']}/assets/images/pieone-logo.png")
        Window.maximize()

        if not os.path.exists(
            f"{os.environ['PIEONE_ROOT']}/simulator.ini"):
            self.config = self.build_config(
                ConfigParser(name='simulator'))
            self.config.read(
                f"{os.environ['PIEONE_ROOT']}/configs/default.ini")
            self.config.update_config(
                f"{os.environ['PIEONE_ROOT']}/simulator.ini", overwrite=True)
            self.config.read(
                f"{os.environ['PIEONE_ROOT']}/simulator.ini")
        else:
            self.config.read(
                f"{os.environ['PIEONE_ROOT']}/simulator.ini")

        self.locale = self.config.get('System', 'locale')
        self.tr.switch_lang(self.locale)
        self.darkmode = self.config.get('Graphics', 'darkmode')
        self.set_theme_style(self.darkmode)
        
        return self.manager_screen
    
    def stop_callback(self):
        button_no = MDRaisedButton(
            text=self.tr._("No"),
            )
        button_yes = MDFlatButton(
            text=self.tr._("Yes"),
            text_color=self.theme_cls.primary_color,
            )
        leave_simulation_dialog = MDDialog(
            title=self.tr._("Exit"),
            text=self.tr._("Do you wish to close the application?"),
            type="simple",
            buttons=[
                button_yes,
                button_no,
            ],
            radius=[20, 7, 20, 7],
        )
        def yes_callback(*args):
            self.stop()
        button_no.on_release = lambda: leave_simulation_dialog.dismiss()
        button_yes.on_release = yes_callback
        leave_simulation_dialog.open()

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
        self.theme_cls.primary_palette = (
            "Orange" if self.theme_cls.primary_palette == "Blue" else "Blue"
        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )
    
    def open_restart_dialog(self):
        if not self.restart_dialog:
            button_ok = MDFlatButton(
                text=self.tr._("Ok"),
                text_color=self.theme_cls.primary_color,
                )
            button_cancel= MDRaisedButton(
                text=self.tr._("Cancel"),
                )
            self.restart_dialog = MDDialog(
                title=self.tr._('Restart required'),
                type="simple",
                text=self.tr._("For changes to take effect application has to restart."),
                buttons=[
                    button_ok,
                    button_cancel,
                ],
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
            )
            def ok_callback(*args):
                self.restart_dialog.dismiss()
                # self.restart(self)
            def cancel_callback(*args):
                self.restart_dialog.dismiss()
            button_ok.on_release=ok_callback
            button_cancel.on_release=cancel_callback
        self.restart_dialog.open()
    
    def open_language_dialog(self):
        if not self.language_dialog:
            button_ok = MDFlatButton(
                text=self.tr._("Ok"),
                text_color=self.theme_cls.primary_color,
                )
            # button_cancel= MDRaisedButton(
            #     text=self.tr._("Cancel"),
            #     )
            temp_lang_selector = self.tr.lang
            def set_language(lang):
                self.locale = lang
                self.tr.switch_lang(self.locale)
            self.language_dialog = MDDialog(
                title=self.tr._('Application language'),
                type="confirmation",
                size_hint=(0.8, 0.8),
                items=[
                    ItemConfirm(text="English (USA)", on_release=lambda x: set_language("en")),
                    ItemConfirm(text="Русский (Россия)", on_release=lambda x: set_language("ru")),
                ],
                buttons=[
                    button_ok,
                    # button_cancel,
                ],
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                height=Window.height + dp(10),
            )
            def ok_callback(*args):
                self.language_dialog.dismiss()
                self.open_restart_dialog()
            # def cancel_callback(*args):
            #     self.language_dialog.dismiss()
            button_ok.on_release=ok_callback
            # button_cancel.on_release=cancel_callback
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
    
    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))
        if section == "Graphics":
            if key == "darkmode":
                self.config.set('Graphics', 'darkmode', value)
                self.darkmode = value
                self.set_theme_style(self.darkmode)
        if section == "System":
            if key == "locale":
                self.locale = value
                self.config.set('System', 'locale', value)
                self.tr.switch_lang(self.locale)
        self.config.write()

    def on_stop(self):
        self.config.set('Graphics', 'darkmode', self.darkmode)
        self.config.set('System', 'locale', self.locale)
        # self.config.update_config(
            # f"{os.environ['PIEONE_ROOT']}/simulator.ini", overwrite=True)
        # with open(f"{os.environ['PIEONE_ROOT']}/simulator.ini", "wt") as config_file:
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

def main(*args, **kwargs):
    SimulatorApp().run()

if __name__ == '__main__':
    main()
