from dataclasses import dataclass
import os
import random
from functools import partial

from kivy.resources import resource_add_path, resource_find
from View.common.app_screen import BaseAppScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.properties import (
    ListProperty, NumericProperty, StringProperty,
    ObjectProperty, BooleanProperty)
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import (
    MDFlatButton, MDIconButton, MDRaisedButton,
    MDRectangleFlatButton)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tooltip import MDTooltip
from kivy.core.window import Window
from kivymd.uix.list import ThreeLineAvatarListItem
from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.banner import MDBanner
from kivymd.uix.label import MDLabel
from kivymd.uix.widget import MDWidget
from kivy.clock import Clock
import time
from datetime import datetime
from View.SimulatorScreen.events import EventManager, Event

class TextClock(MDLabel):
    time = StringProperty('00:00:00')

class EventSnackBar(BaseSnackbar):
    
    header = StringProperty(None)
    text = StringProperty(None)
    font_size = NumericProperty("15sp")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

class TouchHoverArea(MDFlatButton, MDTooltip):
    
    screen = ObjectProperty()
    controls = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def open_command_panel_dialog(self, *args):
        event_text = self.screen.emitted_event.text if self.screen.emitted_event.text else self.app.tr._('Unexpected malfunction')

        def skip_callback(*args):
            self.screen.decisions_dialog.dismiss()
            self.screen.event_snack_bar.dismiss()
            self.screen.solve_event(self.screen.emitted_event, None, None)
            self.screen.switch_event()

        def cancel_callback(*args):
            self.screen.decisions_dialog.dismiss()
            self.screen.event_snack_bar.dismiss()

        command_panel = CommandInterface(
            [ch for i, ch in enumerate(EventManager().choises) if i+1 in self.controls],
            [cm for i, cm in enumerate(EventManager().commands) if i+1 in self.controls],
            event_text)
        command_panel.command_callback = self.screen.command_callback
        command_panel.event_str = [self.tooltip_text, event_text]
        
        self.screen.decisions_dialog_buttons = [
            SkipDecisionDialogButton(close_fn=skip_callback),
            CancelDecisionDialogButton(close_fn=cancel_callback)
        ]
        self.screen.decisions_dialog = DecisionDialog(
            parent_widget=self.screen,
            content_cls=command_panel
            )

        self.screen.decisions_dialog.open(self.screen)

class ControlButton(MDFlatButton):
    
    control = ListProperty([])
    command_callback = ObjectProperty()
    raw_text_str = StringProperty('Control')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

        self.on_release = self._control_callback

    def _control_callback(self, *args):
        self.command_callback(self.control[0], self.control[1])

class CommandInterface(MDBoxLayout):
    
    command_callback = ObjectProperty()
    keypad = ObjectProperty()
    event_str = ListProperty(['', ''])
    
    def __init__(self, button_texts:list, button_commands:list, event_str: list, **kwargs):
        super().__init__(**kwargs)
        
        assert len(button_texts)==len(button_commands)
        
        self.app = MDApp.get_running_app()
        self.keypad = self.ids.keypad
        self.event_str = event_str if event_str else [self.app.tr._('Unexpected malfunction'), '']

        for tx, cm in zip(
            button_texts,
            button_commands):
            self.keypad.add_widget(
                ControlButton(
                    raw_text_str=tx,
                    text_color=(1, 1, 1, 1),
                    width=self.keypad.width,
                    control=(cm[0], cm[1]),
                    command_callback=self.callback,
                )
            )

    def callback(self, node, command):
        self.command_callback(node, command)

class EventsList(BoxLayout):
    
    def __init__(
        self,
        items,
        **kwargs):
        super().__init__(**kwargs)
        for item in items:
            self.ids.scroll.add_widget(item)

class EventListItem(ThreeLineAvatarListItem):
    
    icon = StringProperty('close-octagon')
    header = StringProperty("")
    result = StringProperty("")
    answer = StringProperty("", nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

class OkTrackRecordDialogButton(MDRaisedButton):
    
    parent_widget = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

class TrackRecordDialog(MDDialog):
    
    parent_widget = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.buttons = self.parent_widget.track_record_dialog_buttons

class SaveFinishDialogButton(MDFlatButton):
    
    close_fn = ObjectProperty()
    
    def __init__(self, close_fn, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.close_fn = close_fn
        self.on_release = self._callback
    
    def _callback(self):
        try:
            self.close_fn()
        except: 
            self.app.log_callback(self, "FatalError: SaveFinishDialogButton.close_fn could not be executed")

class OkFinishDialogButton(MDRaisedButton):
    
    close_fn = ObjectProperty()
    
    def __init__(self, close_fn, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.close_fn = close_fn
        self.on_release = self._callback
    
    def _callback(self):
        try:
            self.close_fn()
        except: 
            self.app.log_callback(self, "FatalError: OkFinishDialogButton.close_fn could not be executed")

class FinishDialog(MDDialog):
    
    parent_widget = ObjectProperty()
    events_solved = NumericProperty()
    total_time = StringProperty()
    mean_time = NumericProperty()
    accuracy = NumericProperty()
    confidence = NumericProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.buttons = self.parent_widget.finish_dialog_buttons

class SkipDecisionDialogButton(MDFlatButton):
    
    close_fn = ObjectProperty()
    
    def __init__(self, close_fn, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.close_fn = close_fn
        self.on_release = self._callback

    def _callback(self):
        try:
            self.close_fn()
        except: 
            self.app.log_callback(self, "FatalError: SkipDecisionDialogButton.close_fn could not be executed")

class CancelDecisionDialogButton(MDRaisedButton):
    
    close_fn = ObjectProperty()
    
    def __init__(self, close_fn, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.close_fn = close_fn
        self.on_release = self._callback

    def _callback(self):
        try:
            self.close_fn()
        except: 
            self.app.log_callback(self, "FatalError: CancelDecisionDialogButton.close_fn could not be executed")

class DecisionDialog(MDDialog):
    
    parent_widget = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.buttons = self.parent_widget.decisions_dialog_buttons

class SimulatorContent(MDBoxLayout):
    # One-session properties
    solved_events = ListProperty([])
    scheduled_events = ListProperty([])
    emitted_event = ObjectProperty()
    task_timer = ObjectProperty()
    event_clock = ObjectProperty()
    timer_update_clock = ObjectProperty()
    start_time = ObjectProperty()
    is_stopped = BooleanProperty(True)
    is_paused = BooleanProperty(False)
    max_time = NumericProperty(90)
    event_remaining_time = NumericProperty(0)

    # UI suppliments
    blobs = ListProperty([])
    track_record_dialog_buttons = ListProperty([])
    finish_dialog_buttons = ListProperty([])
    decisions_dialog_buttons = ListProperty([])
    event_snack_bar_buttons = ListProperty([])
    decisions_dialog = ObjectProperty()
    track_record_dialog = ObjectProperty()
    finish_dialog = ObjectProperty()
    event_snack_bar = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
        self.event_remaining_time = self.max_time

    def create_schedule(self):
        for event in EventManager().build().events:
            self.scheduled_events.append(event)
        random.shuffle(self.scheduled_events)

    def solve_event(self, event: Event, node, command):
        total_time = self.max_time - self.event_remaining_time
        event.update(node, command, total_time)
        self.solved_events.append(event)
        self.ids.image.source = resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\mnemo_bare.png")

    def timer_callback(self, dt=None) -> None:
        if self.emitted_event:
            self.solve_event(self.emitted_event, None, None)
        self.switch_event()

    def __disable_touch_areas(self, *args) -> None:
        for bl in [
            self.ids.BLOB1,
            self.ids.BLOB2,
            self.ids.BLOB3,
            self.ids.BLOB4,
            self.ids.BLOB5,
            self.ids.BLOB6,
            self.ids.BLOB7,
            self.ids.BLOB8,
            self.ids.BLOB9,
            self.ids.BLOB10,
            self.ids.BLOB11,
            self.ids.BLOB12,
            self.ids.BLOB13,
            self.ids.BLOB14,
            self.ids.BLOB15,
            self.ids.BLOB16,
        ]:
            bl.disabled = True
    
    def __enable_touch_areas(self, *args) -> None:
        for bl in [
            self.ids.BLOB1,
            self.ids.BLOB2,
            self.ids.BLOB3,
            self.ids.BLOB4,
            self.ids.BLOB5,
            self.ids.BLOB6,
            self.ids.BLOB7,
            self.ids.BLOB8,
            self.ids.BLOB9,
            self.ids.BLOB10,
            self.ids.BLOB11,
            self.ids.BLOB12,
            self.ids.BLOB13,
            self.ids.BLOB14,
            self.ids.BLOB15,
            self.ids.BLOB16,
        ]:
            bl.disabled = False
    
    def __pop_event(self):
        if len(self.scheduled_events) > 0:
            self.emitted_event = self.scheduled_events.pop()
            self.ids.image.source = self.emitted_event.gif_path
            self.event_callback(self.emitted_event)
        else:
            events_solved = len(self.solved_events)
            mean_time = sum([event.timing / events_solved for event in self.solved_events if not event.not_attempted])
            total_anwered = sum([0 if event.not_attempted else 1 for event in self.solved_events])
            if total_anwered > 0:
                accuracy = sum([1 if event.is_solved else 0 for event in self.solved_events]) * 100 / total_anwered
            else:
                accuracy = 0.0
            confidence =  total_anwered * 100 / events_solved
            timedelta = datetime.now() - self.start_time
            ellapsed_time = time.gmtime(timedelta.total_seconds())
            total_time = time.strftime('%H%M:%S', ellapsed_time)

            if not self.finish_dialog:
                def dismiss_and_stop(*args):
                    self.finish_dialog.dismiss()
                    self.stop_sim()
                
                def go_to_save_dialog(*args):
                    self.stop_sim()
                    self.app.unsaved_progress = True
                    self.finish_dialog.dismiss()
                    self.app.manager_screen.switch_screen("registration")

                self.finish_dialog_buttons = [
                    SaveFinishDialogButton(close_fn=lambda: go_to_save_dialog()),
                    OkFinishDialogButton(close_fn=lambda:  dismiss_and_stop())]
                self.finish_dialog = FinishDialog(
                    parent_widget=self,
                    events_solved=events_solved,
                    total_time=total_time,
                    mean_time=mean_time,
                    accuracy=accuracy,
                    confidence=confidence,
                    )
            self.app.set_user_data({
                'events_solved': events_solved,
                'total_time': total_time,
                'mean_time': mean_time,
                'accuracy': accuracy,
                'confidence': confidence
            })
            self.finish_dialog.open(self)
    
    def switch_event(self):
        if self.event_snack_bar:
            self.event_snack_bar.dismiss()
        self.event_remaining_time = self.max_time
        self.__reset_clocks()
        self.__pop_event()

    def event_callback(self, event) -> None:
        self.event_snack_bar = EventSnackBar(
            header=event.text,
            text=event.secondary_text,
            snackbar_x="10dp",
            snackbar_y="10dp",
            auto_dismiss=True,
            theme_cls=self.app.theme_cls,
            
            size_hint_x=(
                Window.width - (10 * 2)
            ) / Window.width)
        
        def skip_callback(*agrs):
            self.event_snack_bar.dismiss()
            self.solve_event(self.emitted_event, None, None)
            self.switch_event()

        self.event_snack_bar.buttons = [
            MDFlatButton(
                text=self.app.tr._("SKIP"),
                text_color=(1, 1, 1, 1),
                on_release=skip_callback,
            ),
            MDFlatButton(
                text=self.app.tr._("CLOSE"),
                text_color=(1, 1, 1, 1),
                on_release=self.event_snack_bar.dismiss,
            ),
        ]
        self.event_snack_bar.open()

    def update_time(self, dt=None):
        timedelta = datetime.now() - self.start_time
        ellapsed_time = time.gmtime(timedelta.total_seconds())
        self.ids.clock.time = time.strftime('%H:%M:%S', ellapsed_time)
        if not self.is_stopped:
            self.event_remaining_time -= 1

    def run_sim(self) -> None:
        if len(self.scheduled_events) == 0:
            self.create_schedule()
        self.ids.button_start.disabled = True
        self.ids.button_pause.disabled = False
        self.ids.button_restart.disabled = False
        self.ids.button_stop.disabled = False
        self.app.unsaved_progress = True

        if self.is_stopped:
            self.event_remaining_time = self.max_time
            self.start_time = datetime.now()
            self.is_stopped = False
            self.__pop_event()
        self.__reset_clocks()
        self.__enable_touch_areas()

    def __reset_clocks(self):
        if not self.is_paused:
            self.event_remaining_time = self.max_time
            self.is_paused = False
        if self.event_clock:
            self.event_clock.cancel()
        if self.timer_update_clock:
            self.timer_update_clock.cancel()
        self.timer_update_clock = Clock.schedule_interval(self.update_time, 1)
        self.event_clock = Clock.schedule_interval(self.timer_callback, self.event_remaining_time)

    def pause_sim(self) -> None:
        self.event_clock.cancel()
        self.timer_update_clock.cancel()
        self.is_paused = True
        self.__disable_touch_areas()
        self.ids.button_start.disabled = False
        self.ids.button_pause.disabled = True
        self.ids.button_restart.disabled = False
        self.ids.button_stop.disabled = False
    
    def restart_sim(self) -> None:
        self.stop_sim()
        self.run_sim()

    def stop_sim(self) -> None:
        if self.event_clock:
            self.event_clock.cancel()
        if self.timer_update_clock:
            self.timer_update_clock.cancel()
        self.__disable_touch_areas()
        self.scheduled_events.clear()
        self.solved_events.clear()
        self.ids.clock.time = '00:00:00'
        self.is_stopped = True
        # self.emitted_event
        self.ids.button_start.disabled = False
        self.ids.button_pause.disabled = True
        self.ids.button_restart.disabled = True
        self.ids.button_stop.disabled = True
        self.ids.image.source = resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\mnemo_bare.png")
        self.app.unsaved_progress = False
    
    def command_callback(self, node, command) -> None:
        self.event_snack_bar.dismiss()
        self.decisions_dialog.dismiss()
        self.event_clock.cancel()
        self.timer_update_clock.cancel()
        self.solve_event(self.emitted_event, node, command)
        self.switch_event()

    def show_track_record(self) -> None:
        
        button = OkTrackRecordDialogButton(parent_widget=self.track_record_dialog)
        button.on_release = lambda: self.track_record_dialog.dismiss()
        self.track_record_dialog_buttons = [button]
        
        content=EventsList(
                [
                    EventListItem(
                        icon="check-decagram" if event.is_solved==True else "transit-skip" if event.not_attempted==True else "close-octagon",
                        # icon_left_color=(0, 1, 0, 1) if event.is_solved==True else (0, 0, 1, 1) if event.not_attempted==True else (1, 0, 0, 1),
                        header=event.text,
                        result=event.tertiary_text,
                        answer=event.answer if event.answer else ""
                    ) for event in self.solved_events
                ],
            )
        
        self.track_record_dialog = TrackRecordDialog(parent_widget=self, content_cls=content)
        self.track_record_dialog.open(self)

class SimulatorScreenView(BaseAppScreen):
    screen_content = SimulatorContent

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)