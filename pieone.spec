# -*- mode: python -*-
import os

from kivy_deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks
from kivymd import hooks_path as kivymd_hooks_path
root_path = os.path.abspath(os.path.dirname("app.py"))
block_cipher = None
# from .appversion import __dev_version__, __rel_version__

added_files = [
         # Basic
         ( 'README.rst', '.' ),
         ( 'LICENSE', '.' ),
         
         # Application Screens
         ( 'app.kv', '.' ),
         ( 'View/AboutScreen/about_screen.kv', 'View/AboutScreen/' ),
         ( 'View/DocumentationScreen/documentation_screen.kv', 'View/DocumentationScreen/' ),
         ( 'View/RegistrationScreen/registration_screen.kv', 'View/RegistrationScreen/' ),
         ( 'View/SchematicScreen/schematic_screen.kv', 'View/SchematicScreen/' ),
         ( 'View/SimulatorScreen/simulator_screen.kv', 'View/SimulatorScreen/' ),
         ( 'View/SimulatorScreen/events.kv', 'View/SimulatorScreen/' ),
         ( 'View/common/app_screen.kv', 'View/common/' ),
         ( 'View/common/tbr_screen.kv', 'View/common/' ),
         ( 'View/common/error_screen.kv', 'View/common/' ),
         ( 'View/common/dots/dots.kv', 'View/common/dots/' ),
         ( 'View/MenuScreen/menu_screen.kv', 'View/MenuScreen/' ),
         ( 'View/MenuScreen/components/card/card.kv', 'View/MenuScreen/components/card/' ),

         # Documentation
         ( 'docs/en/2-Simulator/1-Beginning.rst', 'docs/en/2-Simulator/' ),
         ( 'docs/en/3-For_developers/1-Developing_simulators.rst', 'docs/en/3-For_developers/' ),
         ( 'docs/en/3-For_developers/2-Writing_documentation.rst', 'docs/en/3-For_developers/' ),
         ( 'docs/en/1-Getting_Started.rst', 'docs/en/' ),

         # Assets
         ## Locales
         ( 'assets/locales/en/LC_MESSAGES/pieone.mo', 'assets/locales/en/LC_MESSAGES/' ),
         ( 'assets/locales/ru/LC_MESSAGES/pieone.mo', 'assets/locales/ru/LC_MESSAGES/' ),
         ## Images
         ( 'assets/images/loading.gif', 'assets/images/' ),
         ( 'assets/images/image-broken.png', 'assets/images/'),
         ( 'assets/images/logo32.png', 'assets/images/' ),
         ( 'assets/images/logo64.png', 'assets/images/' ),
         ( 'assets/images/logo256.png', 'assets/images/' ),
         ( 'assets/images/pieone-logo.png', 'assets/images/' ),
         ( 'assets/images/pieone-splash.png', 'assets/images/' ),
         ( 'assets/images/about_screen/logo.png', 'assets/images/about_screen/' ),
         ( 'assets/images/menu_screen/about-dark.png', 'assets/images/menu_screen/' ),
         ( 'assets/images/menu_screen/about.png', 'assets/images/menu_screen/' ),
         ( 'assets/images/menu_screen/documentation-dark.png', 'assets/images/menu_screen/' ),
         ( 'assets/images/menu_screen/documentation.png', 'assets/images/menu_screen/' ),
         ( 'assets/images/menu_screen/schematic-dark.png', 'assets/images/menu_screen/' ),
         ( 'assets/images/menu_screen/schematic.png', 'assets/images/menu_screen/' ),
         ( 'assets/images/menu_screen/simulator-dark.png', 'assets/images/menu_screen/' ),
         ( 'assets/images/menu_screen/simulator.png', 'assets/images/menu_screen/' ),
         ( 'assets/images/schematic_screen/mnemo_st0.png', 'assets/images/schematic_screen/' ),
         ( 'assets/images/schematic_screen/mnemo_st1.png', 'assets/images/schematic_screen/' ),
         ( 'assets/images/schematic_screen/mnemo_st2.png', 'assets/images/schematic_screen/' ),
         ( 'assets/images/schematic_screen/mnemo_st3.png', 'assets/images/schematic_screen/' ),
         ( 'assets/images/schematic_screen/mnemo_st4.png', 'assets/images/schematic_screen/' ),
         ( 'assets/images/schematic_screen/mnemo_st5.png', 'assets/images/schematic_screen/' ),
         ( 'assets/images/schematic_screen/mnemo_st6.png', 'assets/images/schematic_screen/' ),
         ( 'assets/images/simulator_screen/CO_1_high_level.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/CO_1_low_level.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/CO_2_high_level.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/CO_2_low_level.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/compressor_1.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/compressor_2.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/furnace.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/mnemo_bare.png', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/pump_1.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/pump_2.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/reactor_1.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/reactor_2.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/separator_1_high_pressure.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/separator_1_low_level.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/separator_1_overflow.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/separator_2_high_pressure.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/separator_2_low_level.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/separator_2_overflow.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/tower_1.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/vent_1.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/vent_2.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/vent_3.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/vessel_1_high_pressure.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/vessel_1_low_level.gif', 'assets/images/simulator_screen/' ),
         ( 'assets/images/simulator_screen/vessel_1_overflow.gif', 'assets/images/simulator_screen/' ),
         
         ## icons
         ( 'assets/icons/logo32.ico', 'assets/icons/' ),
         ( 'assets/icons/logo64.ico', 'assets/icons/' ),
         ( 'assets/icons/logo256.ico', 'assets/icons/' ),

         ## data
         ( 'assets/data/about_screen/about.txt', 'assets/data/about_screen/' ),
         ( 'assets/data/schematic_screen/sc1_desc.txt', 'assets/data/schematic_screen/' ),
         ( 'assets/data/schematic_screen/sc2_desc.txt', 'assets/data/schematic_screen/' ),
         ( 'assets/data/schematic_screen/sc3_desc.txt', 'assets/data/schematic_screen/' ),
         ( 'assets/data/schematic_screen/sc4_desc.txt', 'assets/data/schematic_screen/' ),
         ( 'assets/data/schematic_screen/sc5_desc.txt', 'assets/data/schematic_screen/' ),
         ( 'assets/data/schematic_screen/sc6_desc.txt', 'assets/data/schematic_screen/' ),
         ( 'assets/data/schematic_screen/sc7_desc.txt', 'assets/data/schematic_screen/' ),

         # Configs
         ( 'configs/default.ini', 'configs/' ),
         ( 'configs/graphics.json', 'configs/' ),
         ( 'configs/system.json', 'configs/' ),
         ]

a = Analysis(['app.py'],
            #  binaries=[],
             datas=added_files,
            #  hiddenimports=[],
            hookspath=hookspath()+[kivymd_hooks_path],
             runtime_hooks=runtime_hooks(),
            #  excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False,
             **get_deps_minimal()
             )
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='pieone',
          icon="assets\icons\logo256.ico",
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          argv_emulation=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          )
coll = COLLECT(exe, #Tree(root_path),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='pieone')
