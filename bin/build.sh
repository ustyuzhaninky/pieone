#!/bin/bash
venv=$(cat config.json | jq '.venv')
activate=$venv/bin/activate
deactivate=$venv/bin/deactivate

echo "Working with virtual environment as $venv"
source $venv/bin/activate
pip install -r requirements-dev.txt
python -m PyInstaller pieone.spec --noconfirm --log-level=WARN --workpath ./build/Linux --distpath ./dist/Linux
source $venv/bin/deactivate