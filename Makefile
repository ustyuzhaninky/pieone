PYTHON = python
CHECKSCRIPT = tools/pep8checker/pep8kivy.py
KIVY_DIR =
KIVY_USE_DEFAULTCONFIG = 1
HOSTPYTHON = $(KIVYIOSROOT)/tmp/Python-$(PYTHON_VERSION)/hostpython
IOSPATH := $(PATH):/Developer/Platforms/iPhoneOS.platform/Developer/usr/bin
NOSETESTS = $(PYTHON) -m nose.core

.PHONY: po mo hook style stylereport test help

po:
	xgettext -Lpython --output=assets/locales/messages.pot app.py \
	View/common/app.kv \
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
	touch assets/locales/en/po/en.po
	touch assets/locales/ru/po/ru.po
	msgmerge --output-file=assets/locales/en/po/en.po assets/locales/en/po/en.po assets/locales/messages.pot
	msgmerge --output-file=assets/locales/ru/po/ru.po assets/locales/ru/po/ru.po assets/locales/messages.pot

mo:
	mkdir -p assets/locales/en/LC_MESSAGES
	msgfmt -c -o assets/locales/en/LC_MESSAGES/pieone.mo assets/locales/en/po/en.po
	msgfmt -c -o assets/locales/ru/LC_MESSAGES/pieone.mo assets/locales/ru/po/ru.po

hook:
	# Install pre-commit git hook to check your changes for styleguide
	# consistency.
	cp tools/pep8checker/pre-commit.githook .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

style:
	$(PYTHON) $(CHECKSCRIPT) .

stylereport:
	$(PYTHON) $(CHECKSCRIPT) -html .

test:
	-rm -rf kivy/tests/build
	$(NOSETESTS) tests

build:
	python -m PyInstaller --noconfirm --log-level=WARN pieone.spec

release:
	python -m PyInstaller --noconfirm --log-level=WARN pieone.spec

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  hook           add Pep-8 checking as a git precommit hook"
	@echo "  style          to check Python code for style hints."
	@echo "  style-report   make html version of style hints"
	@echo "  testing        make unittest (nosetests)"
	@echo "  build 			make a build with PyInstaller"
	@echo "  release		make a release package with PyInstaller"
