# Project Setup Guide

This guide will help you set up the development environment for this project.

## Prerequisites
- Python 3.8 or newer
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- Git (for version control)

## Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd <project-directory>
   ```

2. **Install dependencies using uv**
   ```bash
   uv pip install -r requirements.txt
   # or, if using pyproject.toml:
   uv pip install -r pyproject.toml
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## Additional Notes
- If you add new dependencies, update `pyproject.toml` and run:
  ```bash
  uv pip install <package-name>
  uv pip freeze > uv.lock
  ```
- For more information on `uv`, see the [uv documentation](https://github.com/astral-sh/uv).

## Troubleshooting
- Ensure you are using the correct Python version.
- If you encounter issues with dependencies, try removing the `.venv` folder (if present) and reinstalling.

---

Feel free to reach out to the project maintainer for further assistance.
