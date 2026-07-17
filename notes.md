# 🗺️ Roadtrip AI: Project Setup

This guide outlines the quick-start instructions to initialize the `roadtrip-ai` development environment using **uv**.

## 🚀 Quick Start

### 1. Create the Project Directory
Navigate to your desktop and create a new folder for the project:
```bash
cd ~/Desktop
mkdir roadtrip-ai
cd roadtrip-ai
```

### 2. Initialize the Project
Initialize a new Python application managed by `uv`:
```bash
uv init
```

### 3. Configure the Python Runtime
Install and lock the project to Python 3.12:
```bash
uv python install 3.12
uv python pin 3.12
```

### 4. Install Dependencies
Add the required production and development dependencies to the project:

**Production Dependencies:**
```bash
uv add fastapi uvicorn httpx pydantic-settings
```

**Development Dependencies:**
```bash
uv add --dev pytest ruff
```

### 5. Run the Application
Start the application using the `uv` virtual environment runner:
```bash
uv run python main.py
```
