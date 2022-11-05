from genericpath import isfile
import os
import pathlib
from turtle import onclick
# from View.DocumentationScreen.md_cefbrowser import MDCefBrowser
# TODO: Add support of real browsing using CEF

from View.common.app_screen import BaseAppScreen
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.navigationdrawer import (
    MDNavigationDrawerMenu, MDNavigationDrawerLabel,
    MDNavigationDrawerDivider, MDNavigationDrawerHeader,
    MDNavigationDrawerItem, 
)
from kivy.properties import OptionProperty, DictProperty
from kivy.event import EventDispatcher
# import markdown
from kivy.clock import Clock
from functools import partial
from kivy.uix.rst import RstDocument

class BaseNavigationDrawerItem(MDNavigationDrawerItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = 24
        self.text_color = "#4a4939"
        self.icon_color = "#4a4939"
        self.focus_color = "#e7e4c0"


class DrawerLabelItem(BaseNavigationDrawerItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.focus_behavior = False
        self._no_ripple_effect = True
        self.selected_color = "#4a4939"


class DrawerClickableItem(BaseNavigationDrawerItem):
    def __init__(self, file_name, **kwargs):
        super().__init__(**kwargs)
        self.ripple_color = "#c5bdd2"
        self.selected_color = "#0c6c4d"
        self.file_name = file_name

class DocumentationScreenView(BaseAppScreen, EventDispatcher):

    lang_folder = OptionProperty("en", options=["en", "ru"])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        doc_folder = os.path.join(f"{os.environ['PIEONE_ROOT']}", "docs")

        def parse_folder(path):
            for it in sorted(os.listdir(path)):
                if os.path.isfile(os.path.join(path, it)):
                    self.ids.nav_drawer_menu.add_widget(
                        DrawerClickableItem(
                            icon='file-document',
                            text=it.split('.')[0].replace('_', ' ').split('-')[-1],
                            on_release=self.show_md_file,
                            file_name=os.path.join(path, it)
                            )
                    )
                else:
                    self.ids.nav_drawer_menu.add_widget(
                        DrawerLabelItem(
                            icon='folder',
                            text=it.split('.')[0].replace('_', ' ').split('-')[-1],
                        )
                    )
                    parse_folder(os.path.join(path, it))
        parse_folder(os.path.join(doc_folder, next(self.get_lang())))

    def lang_callback(self, control, item):
            return control.current_active_segment.text
    
    def get_lang(self):
        if self.ids.lang_segments.current_active_segment:
            yield self.ids.lang_segments.current_active_segment.text
        else:
            yield 'en'

    def on_enter(self) -> None:
        self.show_md_file(
            os.path.join(
                f"{os.environ['PIEONE_ROOT']}",
                "docs", next(self.get_lang()),
                "1-Getting_Started.rst"))
        
        self.ids.box.add_widget(
                MDFloatingActionButton(
                    icon="menu",
                    type='small',
                    on_release=lambda x: self.ids.nav_drawer.set_state("open"),
                ))

    def show_md_file(self, widget) -> None:
        if isinstance(widget, str):
            path = widget
        else:
            path = widget.file_name
            path = os.path.join(
                f"{os.environ['PIEONE_ROOT']}",
                "docs",
                next(self.get_lang()),
                *pathlib.Path(path).parts[
                    len(pathlib.Path(f"{os.environ['PIEONE_ROOT']}").parts) + 2:
                ])
        # path = os.path.join(path, pathlib.Path(widget.file_name).parts[:len])
        if os.path.isfile(path):
            with open(
                path,
                'rt',
                encoding="utf-8",
                ) as md_file:
                text = md_file.read()
                self.ids.browser.clear_widgets()
                document = RstDocument(text=text)
                document.render()
                self.ids.browser.add_widget(document)
        else:
            print(f"Path `{path}` is not a file")
                