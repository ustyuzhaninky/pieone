.PHONY: po mo

po:
	xgettext -Lpython --output=assets/locales/messages.pot app.py app.kv \
	View/AboutScreen/about_screen.kv View/AboutScreen/about_screen.py \
	View/ManagerScreen/manager_screen.py \
	View/MenuScreen/menu_screen.kv View/MenuScreen/menu_screen.py \
	View/SettingsScreen/settings_screen.py \
	View/DocumentationScreen/documentation_screen.kv View/DocumentationScreen/documentation_screen.py \
	View/SchematicScreen/schematic_screen.kv View/SchematicScreen/schematic_screen.py \
	View/SimulatorScreen/simulator_screen.kv View/SimulatorScreen/simulator_screen.py \
	View/common/app_screen.py View/common/app_screen.kv \
	View/SimulatorScreen/events.py View/SimulatorScreen/events.kv \
	View/RegistrationScreen/registration_screen.py View/RegistrationScreen/registration_screen.kv
	msgmerge assets/locales/en/po/en.po assets/locales/messages.pot
	msgmerge assets/locales/ru/po/ru.po assets/locales/messages.pot

mo:
	mkdir -p assets/locales/en/LC_MESSAGES
	msgfmt -c -o assets/locales/en/LC_MESSAGES/pieone.mo assets/locales/en/po/en.po
	msgfmt -c -o assets/locales/ru/LC_MESSAGES/pieone.mo assets/locales/ru/po/ru.po