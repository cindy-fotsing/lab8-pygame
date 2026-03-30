# Lab 8 - Pygame Random Squares

A simple Python + Pygame application that displays 10 colored squares moving randomly on a canvas.

## Features

- Opens an 800x600 window
- Draws 10 squares with random size, color, and initial position
- Moves squares continuously with random velocity
- Occasionally changes square direction for more random motion
- Bounces squares off window edges

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

## Setup

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Close the window to stop the program.

## Project Structure

- `main.py`: Pygame application entry point and animation loop
- `requirements.txt`: Python dependencies
- `README.md`: Project documentation
