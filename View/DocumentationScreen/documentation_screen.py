from genericpath import isfile
import os
import pathlib

from kivy.resources import resource_find
from kivymd.uix.navigationdrawer import (
    MDNavigationDrawerHeader,
    MDNavigationDrawerItem, 
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp # NOQA
from kivy.properties import OptionProperty
from kivy.event import EventDispatcher
from kivy.uix.rst import RstDocument

from View.common.app_screen import BaseAppScreen

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

class DocumentationContent(MDBoxLayout, EventDispatcher):

    lang_folder = OptionProperty("en", options=["en", "ru"])
    
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)

    def parse_folder(self, path: str, lang: str):
        
        def fn_parse(path):
            for it in sorted(os.listdir(path)):
                if os.path.isfile(os.path.join(path, it)):
                    self.ids.nav_drawer_menu.add_widget(
                        DrawerClickableItem(
                            icon='file-document',
                            text=it.split('.')[0].replace('_', ' ').split('-')[-1],
                            on_release=self.show_md_file,
                            file_name=os.path.join(path, it),
                            theme_text_color="Custom",
                            text_color=self.app.theme_cls.text_color
                            )
                    )
                else:
                    self.ids.nav_drawer_menu.add_widget(
                        DrawerLabelItem(
                            icon='folder',
                            text=it.split('.')[0].replace('_', ' ').split('-')[-1],
                        )
                    )
                    fn_parse(os.path.join(path, it))
        
        if len(self.ids.nav_drawer_menu.children[0].children)==0:
            self.ids.nav_drawer_menu.add_widget(
                MDNavigationDrawerHeader(
                    title=self.app.tr._("Documentation"),
                    title_font_size="23sp",
                    # source=resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\logo32.png"),
                    text=self.app.tr._("P.I.E. ONE intergrated\nuser manual"),
                    spacing="4dp",
                    padding=("12dp", 0, 0, "56dp"),
                    size=(2, 2),
                )
            )
            fn_parse(os.path.join(
                    f"{os.environ['PIEONE_ROOT']}",
                    "docs", self.lang_folder))
            self.show_md_file(
                os.path.join(
                    f"{os.environ['PIEONE_ROOT']}",
                    "docs", self.lang_folder,
                    "1-Getting_Started.rst"))
    
    def set_language(self, segmented_control, segmented_item):
        # doc_folder = os.path.join(f"{os.environ['PIEONE_ROOT']}", "docs", self.lang_folder)
        self.lang_folder = segmented_item.text
        self.ids.nav_drawer_menu.children[0].children.clear_widgets()
        doc_folder = os.path.join(f"{os.environ['PIEONE_ROOT']}", "docs", self.lang_folder)
        self.parse_folder(doc_folder, self.lang_folder)

    def populate_drawer(self, *args):
        doc_folder = os.path.join(f"{os.environ['PIEONE_ROOT']}", "docs", self.lang_folder)
        self.parse_folder(doc_folder, self.lang_folder)
        self.ids.nav_drawer.set_state("open")
    
    def show_md_file(self, widget) -> None:
        if isinstance(widget, str):
            path = widget
        else:
            path = widget.file_name
            path = os.path.join(
                f"{os.environ['PIEONE_ROOT']}",
                "docs",
                self.lang_folder,
                *pathlib.Path(path).parts[
                    len(pathlib.Path(f"{os.environ['PIEONE_ROOT']}").parts) + 2:
                ])
        if os.path.isfile(path):
            with open(
                resource_find(path),
                'rt',
                encoding="utf-8",
                ) as md_file:
                text = md_file.read()
                self.ids.browser.clear_widgets()
                document = RstDocument(text=text)
                document.render()
                self.ids.browser.add_widget(document)
        else:
            self.app.log_callback(self, f"Path `{path}` is not a file")

class DocumentationScreenView(BaseAppScreen):
    screen_content = DocumentationContent

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
