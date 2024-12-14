# Equipment Rental System Prototype

## Overview

The **Equipment Rental System Prototype** is a Python-based GUI application designed to manage equipment rentals efficiently. It allows users to add or delete equipment, manage client information, display equipment and client lists, and process rentals seamlessly.

## Features

- **Add/Delete Equipment:** Manage the inventory of rental equipment.
- **Add/Delete Clients:** Manage customer information.
- **Display Equipment/Clients:** View all equipment and client details.
- **Process Rentals:** Assign equipment to clients and track rental transactions with automatic cost calculation.

## Technologies Used

- **Python 3.11.5**
- **Tkinter:** For GUI development.
- **MySQL:** For data storage.
- **mysql-connector-python:** Python library to interact with MySQL.

## Project Structure

- **src/**: Contains all Python source code.
  - **main.py**: Entry point of the application.
  - **models.py**: Defines data models/classes.
  - **data_manager.py**: Handles database interactions.
  - **gui.py**: Manages the GUI components using Tkinter.
- **db/**: Contains SQL scripts for setting up the database.

  - **schema.sql**: Defines the database schema (tables and relationships).
  - **seed_data.sql**: Populates the database with initial data.

- **requirements.txt**: Lists all Python dependencies.
- **README.md**: Project documentation.
- **.gitignore**: Specifies files/directories to be ignored by version control.

## Setup Instructions

### 1. Clone the Repository

Open your terminal or command prompt and execute:

```bash
git clone https://github.com/aulakh-savreet/rental_system.git
cd rental_system
```
