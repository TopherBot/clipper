#!/usr/bin/env bash
set -e
# Install required Python packages into a virtualenv located in .venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pyperclip cryptography
# Make the script executable and add to PATH via alias (optional)
chmod +x clipper.py
# Create a convenient alias if user agrees
read -p "Create a global alias 'clipper'? (y/N) " answer
if [[ $answer == [Yy]* ]]; then
  echo "alias clipper='$(pwd)/clipper.py'" >> ~/.bashrc
  echo "Alias added to ~/.bashrc. Reload your shell or run 'source ~/.bashrc'"
fi
