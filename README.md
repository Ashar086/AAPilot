# AAPilot Project

AAPilot is a Flask-based web application for personality assessment and matchmaking. The application is organized into a modular structure with separate blueprints for different features.

## Project Structure

The project follows a modular blueprint-based architecture:

```
AAPilot/
├── app.py                  # Main application entry point
├── requirements.txt        # Project dependencies
├── assessment/             # Assessment functionality
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── utils.py
│   └── templates/
│       └── assessment/     # Assessment-specific templates
├── auth/                   # Authentication
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
├── core/                   # Core functionality
│   ├── __init__.py
│   ├── database.py
│   ├── routes.py
│   └── templates/
│       ├── core/           # Core-specific templates
│       └── shared/         # Shared templates used by multiple blueprints
├── recipient/              # Recipient-specific functionality
│   ├── __init__.py
│   ├── routes.py
│   └── templates/
│       └── recipient/      # Recipient-specific templates
└── results/                # Results handling
    ├── __init__.py
    ├── models.py
    ├── routes.py
    └── templates/
        └── results/        # Results-specific templates
```

## Features

- Modular architecture with Flask blueprints
- Personality assessment system
- User authentication
- Results analysis and visualization
- Sharing capabilities

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables (create a `.env` file):
   ```
   OPENAI_API_KEY=your_openai_api_key
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_NAME=aa_pilot
   ```
4. Run the application:
   ```
   python app.py
   ```

## Blueprint Structure

Each blueprint follows a consistent structure:

- `__init__.py`: Blueprint initialization
- `routes.py`: Route definitions
- `models.py`: Database models (if applicable)
- `utils.py`: Utility functions (if applicable)
- `templates/`: Blueprint-specific templates

## Template Organization

- Blueprint-specific templates are stored in their respective blueprint's templates directory
- Shared templates used by multiple blueprints are stored in `core/templates/shared/`
