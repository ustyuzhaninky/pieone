from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.toolbar import MDTopAppBar

from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'resizable', True)

Builder.load_string(
    '''
#:import images_path kivymd.images_path
#:import MDTopAppBar kivymd.uix.toolbar

<CustomOneLineIconListItem>

    IconLeftWidget:
        icon: root.icon


<PreviousMDIcons>
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            id: toolbar
            title: "Icon Viewer"
            anchor_title: "left"
            elevation: 12
            adaptive_size: True
            opposite_colors: True
            use_overflow: True
            

        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            padding: dp(20)

            MDBoxLayout:
                adaptive_height: True

                MDIconButton:
                    icon: 'magnify'

                MDTextField:
                    id: search_field
                    hint_text: 'Search icon'
                    on_text: root.set_list_md_icons(self.text, True)

            RecycleView:
                id: rv
                key_viewclass: 'viewclass'
                key_size: 'height'

                RecycleBoxLayout:
                    padding: dp(10)
                    default_size: None, dp(48)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
'''
)


class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()


class PreviousMDIcons(Screen):

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''
        
        self.app = MDApp.get_running_app()
        self.ids.toolbar.right_action_items = [
                ["window-minimize", lambda x: Window.minimize()],
                ["window-maximize", lambda x: Window.maximize()],
                ["close", lambda x: self.app.stop(), "Exit", "Exit"]
                ]

        def add_icon_item(name_icon):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "icon": name_icon,
                    "text": name_icon,
                    "callback": lambda x: x,
                }
            )
        

        self.ids.rv.data = []
        for name_icon in md_icons.keys():
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = PreviousMDIcons()
        # Window.borderless = True

    def build(self):
        return self.screen

    def on_start(self):
        self.screen.set_list_md_icons()


MainApp().run()