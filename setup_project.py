import os
from pathlib import Path

# The name of the root directory can be the project name
# but we are already inside it. So we define the subdirectories.
DIRECTORIES = [
    "assets/sprites",
    "assets/sounds",
    "game/components",
]

# Files that we want to create
FILES = {
    "game/__init__.py": "",
    "game/components/__init__.py": "",
    "config.py": "# This file will hold all game configuration constants.",
    "main.py": "# This is the main entry point for our game.",
}

def setup_project():
    """Creates the project directory structure and initial files."""
    print("Setting up project structure...")

    # Create directories
    for dir_path in DIRECTORIES:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")

    # Create files
    for file_path, content in FILES.items():
        path = Path(file_path)
        if not path.exists():
            with open(path, "w") as f:
                f.write(content)
            print(f"Created file: {file_path}")
        else:
            print(f"File already exists: {file_path}")

    print("\nProject structure successfully created!")
    print("You can now delete this setup_project.py file.")


if __name__ == "__main__":
    setup_project()
