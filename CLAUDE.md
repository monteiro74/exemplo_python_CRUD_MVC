# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python desktop application demonstrating CRUD operations using MVC architecture. It's an educational project for teaching software engineering, database management, and programming concepts. The application manages students (alunos) and pets with a GUI built using CustomTkinter.

## Running the Application

**Main entry point:**
```bash
python main.py
```

The application requires MySQL/MariaDB to be running with proper database configuration.

## Dependencies Installation

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

**Alternative installation scripts:**
- `python instalar_dependencias.py` - General dependency installer
- `python instalar_no_spyder.py` - Spyder IDE specific installer

**Key dependencies:**
- customtkinter==5.2.2
- mysql-connector-python==9.5.0
- Pillow==12.0.0
- matplotlib==3.10.7
- fpdf2==2.8.5

## Database Configuration

**Connection configuration file:** `model/conexao.con`

This file must exist in the `model/` directory and contains database connection parameters in key=value format:
```
host='localhost'
port='3306'
database='nome_do_banco'
user='usuario'
password='senha'
```

**Database setup scripts:** Located in `db_script/`
- `alunos.sql` - Students table (primary table)
- `pets.sql` - Pets table (foreign key to students via CPF)
- `users.sql` - Users table for authentication

The application expects a MySQL/MariaDB database. Run these scripts to create the required tables.

## MVC Architecture

This project strictly follows the MVC pattern:

### Model Layer (`model/`)
- `conexao_db.py` - Database connection management
  - `ler_conexao(arquivo='conexao.con')` - Reads connection config from file
  - `obter_conexao()` - Returns active MySQL connection

### Controller Layer (`controller/`)
Controllers provide CRUD operations and business logic:
- `aluno_controller.py` - Student operations
- `pet_controller.py` - Pet operations
- `user_controller.py` - User/authentication operations
- `grafico_controller.py` - Chart/graph data processing
- `relatorio_controller.py` - Report generation logic

### View Layer (`view/`)
All GUI forms and windows using CustomTkinter:
- `grid_*.py` - Data grid/table views
- `form_*.py` - Data entry and edit forms
- `report_*.py` - Report generation interfaces

**Modal window pattern:** All forms are opened as modal dialogs from main.py:
```python
form = SomeForm(self)
form.transient(self)
form.grab_set()
form.focus_set()
```

## Logging System

**Log file:** `logs/logs.csv`

All system events are logged using `logger.py`:
```python
from logger import log_event
log_event("module_name", "action_description")
```

Log format: `date;time;app_name;method_name`

## Key Features Implementation

### Image Storage
Images are stored as LONGBLOB in the database (e.g., student photos in `alunos.foto` field). The application uses PIL/Pillow for image handling.

### Master-Detail Pattern
`form_mestre_detalhe.py` demonstrates the master-detail UI pattern showing students (master) with their associated pets (detail).

### Reports
Reports are generated as PDF files using fpdf2 library. The main report logic is in `controller/relatorio_controller.py` with UI in `view/report_alunos.py`.

### Charts/Graphs
Charts use matplotlib and are displayed in CustomTkinter windows:
- `form_idade_alunos.py` - Age distribution chart
- `form_quantidade_alunos.py` - Student count chart

### Data Export
CSV export functionality is implemented in `main.py` using Python's csv module.

## Documentation Generation

**Generate technical documentation:**
```bash
python documentador.py
```

This creates `documentacao/documentacao.md` with code documentation, directory structures, and Mermaid diagrams extracted from the project.

## Project Structure Conventions

- **Root files:**
  - `main.py` - Application entry point with main menu and window
  - `logger.py` - Centralized logging utility
  - `documentador.py` - Documentation generator

- **Folders:**
  - `controller/` - Business logic and database operations
  - `view/` - All GUI components
  - `model/` - Database connection (includes `conexao.con` config)
  - `db_script/` - SQL table creation scripts
  - `images/` - Application resources (e.g., `wallpaper.jpg`)
  - `logs/` - Runtime log files
  - `documentacao/` - Generated documentation

## Important Implementation Details

### Error Handling
All database operations and GUI actions use try-except blocks with `messagebox.showerror()` for user feedback.

### Login System
The application requires login on startup via `FormLogin`. The login form is displayed automatically after main window initialization using `self.after(100, self.mostrar_login)`.

### Database Table Relationships
- Students (alunos): Primary key is `matricula` (enrollment number)
- Pets (pets): References students via `cpf_dono` (owner's CPF)
- Students table includes a `cpf` field for this relationship

### CustomTkinter Theme
The application uses light mode: `ctk.set_appearance_mode('light')`

### Background Image
Main window displays `images/wallpaper.jpg` as a resizable background using PIL ImageTk with LANCZOS resampling.

## Common Development Patterns

### Adding a New Form
1. Create form class in `view/form_*.py` inheriting from `ctk.CTkToplevel`
2. Add controller functions in `controller/*_controller.py` for data operations
3. Import and add menu command in `main.py` `configurar_menu()`
4. Use modal pattern: `transient()`, `grab_set()`, `focus_set()`

### Adding New Database Operations
1. Add function to appropriate controller (e.g., `aluno_controller.py`)
2. Use `obter_conexao()` from `model.conexao_db`
3. Always close cursor and connection after operations
4. Use `cursor(dictionary=True)` for dict-based result rows

### Adding Logging
Import and call: `log_event("module_name", "description_of_action")`

## Testing Notes

This project does not include automated tests. It was designed for educational purposes demonstrating desktop application development patterns.

## Platform Notes

The project was developed for Windows desktop environments. It has not been tested on Linux, though it uses cross-platform Python libraries.
