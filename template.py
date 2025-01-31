import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

# List of file paths
list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "rag_app.py",
    "Model/trials.ipynb"
]

# Iterate through the list of files
for filepath in list_of_files:
    # Convert filepath to Path object for easy manipulation
    file_path = Path(filepath)
    
    # Check if the file exists
    if file_path.exists():
        logging.info(f"File already exists: {file_path}")
    else:
        # Create directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create the file
        file_path.touch()
        
        logging.info(f"File created: {file_path}")
