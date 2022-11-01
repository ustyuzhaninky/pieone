import os
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.widget import MDWidget
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.behaviors import DragBehavior
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import (
    MDFlatButton, MDRaisedButton)

class TopBar(MDTopAppBar, DragBehavior):
    
    screen = StringProperty('P.I.E.ONE')
    is_maximized = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

        def theme_callback(*args):
            self.app.darkmode = False if self.app.darkmode else True
            self.app.set_theme_style(self.app.darkmode)

        self.right_action_items = [
            # ["cog", lambda x: self.app.open_settings(), self.app.tr._("Settings"), self.app.tr._("Settings")],
            ["theme-light-dark", theme_callback, self.app.tr._("Dark Mode"), self.app.tr._("Dark Mode")],
            ["translate-variant", lambda x: self.app.open_language_dialog(), self.app.tr._("Language"), self.app.tr._("Language")],
            # ["window-minimize", lambda x: Window.minimize(), "Minimize", "Minimize"],
            # ["window-maximize", lambda x: self.maximize_callback(), "Maximize", "Maximize"],
            ["close", lambda x: self.app.stop_callback(), self.app.tr._("Exit"), self.app.tr._("Exit")]
            ]
        self.left_action_items = [
            ["arrow-left", lambda x: self.return_callback(x), self.app.tr._("Return"), self.app.tr._("Return")],
        ]
        self.icon = f"{os.environ['PIEONE_ROOT']}/assets/images/pieone-logo.png"

    def return_callback(self, widget):
        if self.app.unsaved_progress == True:
            button_cancel = MDRaisedButton(
                text=self.app.tr._("Cancel"),
                )
            button_yes = MDFlatButton(
                    text=self.app.tr._("Yes"),
                    text_color=self.app.theme_cls.primary_color,
                    )
            leave_simulation_dialog = MDDialog(
                title=self.app.tr._("Leaving simulation"),
                text=self.app.tr._("Do you wish to leave the screen? All progress will be lost."),
                type="simple",
                buttons=[
                    button_yes,
                    button_cancel,
                ],
                radius=[20, 7, 20, 7],
            )
            def yes_callback(*args):
                leave_simulation_dialog.dismiss()
                
                self.app.manager_screen.switch_screen("menu")
            button_cancel.on_release = lambda: leave_simulation_dialog.dismiss()
            button_yes.on_release = yes_callback
            leave_simulation_dialog.open()
            return self.app.manager_screen.current
        else:
            self.app.manager_screen.switch_screen("menu")
            return self.app.manager_screen.current

    def maximize_callback(self):
        if self.is_maximized == self.is_maximized:
            self.is_maximized = not self.is_maximized
            Window.maximize()
        else:
            Window.restore()

    def menu_callback(self):
        pass