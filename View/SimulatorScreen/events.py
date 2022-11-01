from dataclasses import dataclass
import os

from kivymd.app import MDApp # NOQA

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
            self.answer = choises[commands.index([node, command])]
        else:
            self.timing = time
            self.is_solved = False
            self.answer = choises[commands.index([node, command])]
        

        if (not node) | (not command):
            self.tertiary_text = app.tr._('NOT ATTEMPTED and wasted ')
            self.not_attempted = True
        elif self.is_solved:
            self.tertiary_text = app.tr._('SOLVED in ')
        else:
            self.tertiary_text = app.tr._('FAILED in ')
        self.tertiary_text += str(self.timing)  + app.tr._(' seconds')

events = [
    Event(
        app.tr._('High Level in Reactor R1'),
        app.tr._('Reactor R1 is overflowing'),
        'p1_feed',
        'slower',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\reactor_1.gif"
    ),
    Event(
        app.tr._('Low Level in reactor R1'),
        app.tr._('Reactor is running dry'),
        'p1_feed',
        'faster',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\reactor_1.gif"
    ),
    Event(
        app.tr._('High Temperature in the Furnace F1'),
        app.tr._('Feed line is overheating in the furnace F1'),
        'fuel',
        'less',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\furnace.gif"
    ),
    Event(
        app.tr._('Low Temperature in the Furnace F1'),
        app.tr._('Output stream of the furnace F1 is too cold'),
        'fuel',
        'more',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\furnace.gif"
    ),
    Event(
        app.tr._('Insufficient crude diesel flow'),
        app.tr._('Pump P1 does not recieve enough liquid in the input'),
        'all',
        'stop',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\pump_1.gif"
    ),
    Event(
        app.tr._('Pump P1 had been shut down'),
        app.tr._('Pump P1 stopped unexpectedly'),
        'reserve_pump',
        'engage',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\pump_1.gif"
    ),
    Event(
        app.tr._('High water level in Coalescer CO1'),
        app.tr._('CO1 is overflowing with water'),
        'water_co1',
        'open',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\CO_1_high_level.gif"
    ),
    Event(
        app.tr._('Low water level in Coalescer CO1'),
        app.tr._('CO1 recieves insufficient feed or feed stream is mostly water'),
        'water_co1',
        'close',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\CO_1_low_level.gif"
    ),
    Event(
        app.tr._('High water level in Coalescer CO2'),
        app.tr._('CO2 is overflowing with water'),
        'water_co1',
        'open',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\CO_2_high_level.gif"
    ),
    Event(
        app.tr._('Low water level in Coalescer CO2'),
        app.tr._('CO2 recieves insufficient feed or feed stream is mostly diesel'),
        'water_co2',
        'close',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\CO_2_low_level.gif"
    ),
    Event(
        app.tr._('Compressor C1 malfunction'),
        app.tr._('Alarm on C1 due to insufficient pressure or liquid on the intake'),
        'reserve_compressor',
        'engage',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\compressor_1.gif"
    ),
    Event(
        app.tr._('Compressor C2 malfunction'),
        app.tr._('Alarm on C2 due to insufficient pressure or liquid on the intake'),
        'reserve_compressor',
        'engage',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\compressor_2.gif"
    ),
    Event(
        app.tr._('Pump 2 had been shut down'),
        app.tr._('Pump P2 stopped unexpectedly'),
        'reserve_pump',
        'engage',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\pump_2.gif"
    ),
    Event(
        app.tr._('Air Cooler AC1 does not spin'),
        app.tr._("AC1's turbine malfunctions"),
        'reserve_cooler',
        'engage',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vent_1.gif"
    ),
    Event(
        app.tr._('Air Cooler AC2 does not spin'),
        app.tr._("AC2's turbine malfunctions"),
        'reserve_cooler',
        'engage',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vent_2.gif"
    ),
    Event(
        app.tr._("Air Cooler AC3 does not spin"),
        app.tr._("AC3's turbine malfunctions"),
        'reserve_cooler',
        'engage',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vent_3.gif"
    ),
    Event(
        app.tr._('High Level in Deodorator tower T2'),
        app.tr._('Deodorator tower T2 is overflowing'),
        'water_t2',
        'open',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\reactor_2.gif"
    ),
    Event(
        app.tr._('Low Level in Deodorator tower T2'),
        app.tr._('Deodorator tower T2 is running dry'),
        'water_t2',
        'close',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\reactor_2.gif"
    ),
    Event(
        app.tr._('High Level in Distillation Tower T1'),
        app.tr._('Distillation tower T1 is overflowing'),
        't1_bottom',
        'open',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\tower_1.gif"
    ),
    Event(
        app.tr._('Low Level in Distillation tower T1'),
        app.tr._('Distillation tower T1 is running dry'),
        't1_bottom',
        'close',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\tower_1.gif"
    ),
    Event(
        app.tr._('Dangerously high pressure in separator S1'),
        app.tr._('Too much gas in separator S1'),
        'hcg_s1',
        'open',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_1_high_pressure.gif"
    ),
    Event(
        app.tr._('Dangerously high pressure in separator S2'),
        app.tr._('Too much gas in separator S2'),
        'sulfide_s2',
        'open',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_2_high_pressure.gif"
    ),
    Event(
        app.tr._('Dangerously high pressure in vessel E1'),
        app.tr._('Too much gas in vessel E1'),
        'e1_gas',
        'open',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vessel_1_high_pressure.gif"
    ),
    Event(
        app.tr._('Low liquid level in separator S1'),
        app.tr._('Separator S1 has no liquid'),
        'water_s1',
        'close',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_1_low_level.gif"
    ),
    Event(
        app.tr._('High liquid level in separator S1'),
        app.tr._('Separator S1 is overflowing'),
        'water_s1',
        'open',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_1_overflow.gif"
    ),
    Event(
        app.tr._('High liquid level in separator S2'),
        app.tr._('Separator S2 is overflowing'),
        'water_s2',
        'open',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_2_overflow.gif"
    ),
    Event(
        app.tr._('Low liquid level in separator S2'),
        app.tr._('Separator S2 has no liquid'),
        'water_s2',
        'close',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\separator_2_low_level.gif"
    ),
    Event(
        app.tr._('Low liquid level in vessel E1'),
        app.tr._('Vessel E1 has no liquid'),
        'e1_water',
        'close',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vessel_1_low_level.gif"
    ),
    Event(
        app.tr._('High liquid level in vessel E1'),
        app.tr._('Vessel E1 is overflowing'),
        'e1_water',
        'open',
        f"{os.environ['PIEONE_ROOT']}\\assets\\images\\simulator_screen\\vessel_1_overflow.gif"
    ),
]

choises = [
    app.tr._("Increase fuel feed to furnace F1"), # 1
    app.tr._("Decrease fuel feed to furnace F1"), # 2
    app.tr._("Increase water removal from coalescer CO1"), # 3
    app.tr._("Decrease water removal from coalescer CO1"), # 4
    app.tr._("Increase water removal from coalescer CO2"), # 5
    app.tr._("Decrease water removal from coalescer CO2"), # 6
    app.tr._("Increase reflux feed to feed line of tower T1 from vessel E1"), # 7
    app.tr._("Decrease reflux feed to feed line of tower T1 from vessel E1"), # 8
    app.tr._("Increase cold hydrogen-containing gas feed from compressor C1 output"), # 9
    app.tr._("Decrease cold hydrogen-containing gas feed from compressor C1 output"), # 10
    app.tr._("Increase hydrogen-containing gas removal from separator S1"), # 11
    app.tr._("Decrease hydrogen-containing gas removal from separator S1"), # 12
    app.tr._("Increase hydrocarbon gas removal from vessel E1"), # 13
    app.tr._("Decrease hydrocarbon gas removal from vessel E1"), # 14
    app.tr._("Increase hydrogen-enriched diesel fraction removal from the Tower T1 bottom"), # 15
    app.tr._("Decrease hydrogen-enriched diesel fraction removal from the Tower T1 bottom"), # 16
    app.tr._("Increase distilled gasoline removal by pump P2"), # 17
    app.tr._("Decrease distilled gasoline removal by pump P2"), # 18
    app.tr._("Increase water removal from Deodorator tower T2"), # 19
    app.tr._("Decrease water removal from Deodorator tower T2"), # 20
    app.tr._("Engage a reserve pump"), # 21
    app.tr._("Engage a reserve compressor"), # 22
    app.tr._("Emergency Stop"), # 23
    app.tr._("Increase hydrogen sulfide gas removal from separator S2"), # 24
    app.tr._("Decrease hydrogen sulfide gas removal from separator S2"), # 25
    app.tr._("Engage a reserve cooler"), # 26
    app.tr._("Increase Pump P1 speed"), # 27
    app.tr._("Decrease Pump P1 speed"), # 28
    app.tr._("Increase Pump P2 speed"), # 29
    app.tr._("Decrease Pump P2 speed"), # 30
    app.tr._("Increase Compressor C1 speed"), # 31
    app.tr._("Decrease Compressor C1 speed"), # 32
    app.tr._("Increase Compressor C2 speed"), # 33
    app.tr._("Decrease Compressor C2 speed"), # 34
    app.tr._("Increase Cooler AC1 speed"), # 35
    app.tr._("Decrease Cooler AC1 speed"), # 36
    app.tr._("Increase Cooler AC2 speed"), # 37
    app.tr._("Decrease Cooler AC2 speed"), # 38
    app.tr._("Increase Cooler AC3 speed"), # 39
    app.tr._("Decrease Cooler AC3 speed"), # 40
    app.tr._("Increase water removal from separator S1"), # 41
    app.tr._("Decrease water removal from separator S1"), # 42
    app.tr._("Increase water removal from separator S2"), # 43
    app.tr._("Decrease water removal from separator S2"), # 44
    app.tr._("Increase water removal from vessel E1"), # 45
    app.tr._("Decrease water removal from vessel E1"), # 46
]

commands = [
    ["fuel", "more"], # 1
    ["fuel", "less"], # 2
    ["water_co1", "open"], # 3
    ["water_co1", "close"], # 4
    ["water_co2", "open"], # 5
    ["water_co2", "close"], # 6
    ["reflux", "open"], # 7
    ["reflux", "close"], # 8
    ["hcg_c1", "open"], # 9
    ["hcg_c1", "close"], # 10
    ["hcg_s1", "open"], # 11
    ["hcg_s1", "close"], # 12
    ["e1_gas", "open"], # 13
    ["e1_gas", "close",], # 14
    ["t1_bottom", "open"], # 15
    ["t1_bottom", "close"], # 16
    ["gasoline", "open"], # 17
    ["gasoline", "close"], # 18
    ["water_t2", "open"], # 19
    ["water_t2", "close"], # 20
    ["reserve_pump", "engage"], # 21
    ["reserve_compressor", "engage"], # 22
    ["all", "stop"], # 23
    ["sulfide_s2", "open"], # 24
    ["sulfide_s2", "close"], # 25
    ["reserve_cooler", "engage"], # 26
    ["p1_feed", "faster"], # 27
    ["p1_feed", "slower"], # 28
    ["p2_feed", "faster"], # 29
    ["p2_feed", "slower"], # 30
    ["c1_feed", "faster"], # 31
    ["c1_feed", "slower"], # 32
    ["c2_feed", "faster"], # 33
    ["c2_feed", "slower"], # 34
    ["cooler_ac1", "faster"], # 35
    ["cooler_ac1", "slower"], # 36
    ["cooler_ac2", "faster"], # 37
    ["cooler_ac2", "slower"], # 38
    ["cooler_ac3", "faster"], # 39
    ["cooler_ac3", "slower"], # 40
    ["water_s1", "open"], # 41
    ["water_s1", "close"], # 42
    ["water_s2", "open"], # 43
    ["water_s2", "close"], # 44
    ["e1_water", "open"], # 45
    ["e1_water", "close"], # 46
]
