#!/bin/bash
echo "KivyMD Project initialization"
read -p "Enter path to the venv folder: " venv
read -p "Enter venv name: " name
read -p "Enter path to python distribution: " pythonpath
folder_venv=$venv/$name
exe_path=$venv/$name/bin/python
activate=$venv/$name/bin/activate
deactivate=$venv/$name/bin/deactivate
echo "Setting up project settings..."
jq -n '{"venv": "\($python)"}' \
  --arg python "$folder_venv" > ./config.json

echo "Creating virtual environment..."
python -m venv $folder_venv
echo "Installing packages..."
source $folder_venv/bin/activate
echo "Working with virtual environment as $folder_venv"
$folder_venv/bin/pip install -r requirements.txt
source $folder_venv/bin/deactivate
echo "Finished. Environment set as $folder_venv"