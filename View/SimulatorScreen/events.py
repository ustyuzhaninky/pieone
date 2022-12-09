from dataclasses import dataclass
import os

from kivymd.app import MDApp # NOQA
from kivymd.uix.widget import MDWidget
from kivy.properties import ListProperty, StringProperty
from kivy.resources import resource_add_path, resource_find

app = MDApp.get_running_app()

@dataclass
class Event:
    
    text: str = None
    secondary_text: str = None
    node: str = None
    command: str = None
    gif_path: str = None

    tertiary_text: str = None
    source: str = None
    is_solved: bool = False
    not_attempted: bool = False
    timing: int = None
    answer: str = None
    
    def __init__(
        self,
        text,
        secondary_text,
        node,
        command,
        gif_path) -> None:
        self.text = text
        self.secondary_text = secondary_text
        self.node = node
        self.command = command
        self.gif_path = gif_path

    def update(self, node: str, command: str, time: int) -> None:
        if (not node) | (not command):
            self.timing = time
            self.is_solved = False
        elif (self.node.lower() == node.lower()) & (self.command.lower() == command.lower()):
            self.timing = time
            self.is_solved = True
            self.answer = EventManager().choises[EventManager().commands.index([node, command])]
        else:
            self.timing = time
            self.is_solved = False
            self.answer = EventManager().choises[EventManager().commands.index([node, command])]
        

        if (not node) | (not command):
            self.tertiary_text = EventManager().skipped_text
            self.not_attempted = True
        elif self.is_solved:
            self.tertiary_text = EventManager().solved_text
        else:
            self.tertiary_text = EventManager().failed_text
        self.tertiary_text += str(self.timing)  + EventManager().time_measure_text

class EventManager(MDWidget):
    choises = ListProperty([])
    commands = ListProperty([])
    event_headers = ListProperty([])
    event_subheaders = ListProperty([])
    failed_text = StringProperty()
    solved_text = StringProperty()
    skipped_text = StringProperty()
    time_measure_text = StringProperty()

    events = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def build(self):
        self.events = [
            Event(
                self.event_headers[0],
                self.event_subheaders[0],
                'p1_feed',
                'slower',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\reactor_1.gif")
            ),
            Event(
                self.event_headers[1],
                self.event_subheaders[1],
                'p1_feed',
                'faster',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\reactor_1.gif")
            ),
            Event(
                self.event_headers[2],
                self.event_subheaders[2],
                'fuel',
                'less',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\furnace.gif")
            ),
            Event(
                self.event_headers[3],
                self.event_subheaders[3],
                'fuel',
                'more',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\furnace.gif")
            ),
            Event(
                self.event_headers[4],
                self.event_subheaders[3],
                'all',
                'stop',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\pump_1.gif")
            ),
            Event(
                self.event_headers[5],
                self.event_subheaders[5],
                'reserve_pump',
                'engage',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\pump_1.gif")
            ),
            Event(
                self.event_headers[6],
                self.event_subheaders[6],
                'water_co1',
                'open',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\CO_1_high_level.gif")
            ),
            Event(
                self.event_headers[7],
                self.event_subheaders[7],
                'water_co1',
                'close',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\CO_1_low_level.gif")
            ),
            Event(
                self.event_headers[8],
                self.event_subheaders[8],
                'water_co1',
                'open',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\CO_2_high_level.gif")
            ),
            Event(
                self.event_headers[9],
                self.event_subheaders[9],
                'water_co2',
                'close',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\CO_2_low_level.gif")
            ),
            Event(
                self.event_headers[10],
                self.event_subheaders[10],
                'reserve_compressor',
                'engage',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\compressor_1.gif")
            ),
            Event(
                self.event_headers[11],
                self.event_subheaders[11],
                'reserve_compressor',
                'engage',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\compressor_2.gif")
            ),
            Event(
                self.event_headers[12],
                self.event_subheaders[12],
                'reserve_pump',
                'engage',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\pump_2.gif")
            ),
            Event(
                self.event_headers[13],
                self.event_subheaders[13],
                'reserve_cooler',
                'engage',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vent_1.gif")
            ),
            Event(
                self.event_headers[14],
                self.event_subheaders[14],
                'reserve_cooler',
                'engage',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vent_2.gif")
            ),
            Event(
                self.event_headers[15],
                self.event_subheaders[15],
                'reserve_cooler',
                'engage',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vent_3.gif")
            ),
            Event(
                self.event_headers[16],
                self.event_subheaders[16],
                'water_t2',
                'open',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\reactor_2.gif")
            ),
            Event(
                self.event_headers[17],
                self.event_subheaders[17],
                'water_t2',
                'close',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\reactor_2.gif")
            ),
            Event(
                self.event_headers[18],
                self.event_subheaders[18],
                't1_bottom',
                'open',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\tower_1.gif")
            ),
            Event(
                self.event_headers[19],
                self.event_subheaders[19],
                't1_bottom',
                'close',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\tower_1.gif")
            ),
            Event(
                self.event_headers[20],
                self.event_subheaders[20],
                'hcg_s1',
                'open',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_1_high_pressure.gif")
            ),
            Event(
                self.event_headers[21],
                self.event_subheaders[21],
                'sulfide_s2',
                'open',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_2_high_pressure.gif")
            ),
            Event(
                self.event_headers[22],
                self.event_subheaders[22],
                'e1_gas',
                'open',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vessel_1_high_pressure.gif")
            ),
            Event(
                self.event_headers[23],
                self.event_subheaders[23],
                'water_s1',
                'close',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_1_low_level.gif")
            ),
            Event(
                self.event_headers[24],
                self.event_subheaders[24],
                'water_s1',
                'open',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_1_overflow.gif")
            ),
            Event(
                self.event_headers[25],
                self.event_subheaders[25],
                'water_s2',
                'open',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_2_overflow.gif")
            ),
            Event(
                self.event_headers[26],
                self.event_subheaders[26],
                'water_s2',
                'close',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_2_low_level.gif")
            ),
            Event(
                self.event_headers[27],
                self.event_subheaders[27],
                'e1_water',
                'close',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vessel_1_low_level.gif")
            ),
            Event(
                self.event_headers[28],
                self.event_subheaders[28],
                'e1_water',
                'open',
                resource_find(f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vessel_1_overflow.gif")
            )
        ]
    
        return self
