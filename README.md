# Singularity Health Project

This project consists of a Django (Python) backend with a GraphQL API and a React (JavaScript) frontend.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Git:** For cloning the repository.
* **Python 3.11:** For the backend. Make sure `pip` for Python 3.11 is also available.
* **Node.js and npm:** For the frontend (Node.js LTS version recommended, which includes npm).
* **Docker and Docker Compose:** (Recommended method) For containerizing and running the application services.
* **PostgreSQL Client:** (Optional, for local native setup if you need to interact with the DB directly)
* **PostgreSQL Server:** (Only for local native setup)

---

## Running the Project with Docker (Recommended)

This is the recommended method for running the project as it handles dependencies and services in isolated containers.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/itsthatdavid/SingularityHealth](https://github.com/itsthatdavid/SingularityHealth)
    cd SINGULARITYHEALTH
    ```

2.  **Set Up Environment Variables:**
    * In the project root directory (`SINGULARITYHEALTH/`), find the `env.example.root` file.
    * Copy it to a new file named `.env`:
        ```bash
        cp env.example.root .env
        ```
    * Open the `.env` file and **update the placeholder values for non-local development**, especially `SECRET_KEY`, `DB_PASSWORD`, and `DJANGO_SUPERUSER_PASSWORD` with strong, unique values. You can keep the provided variables if you are only checking the project.

3.  **Build and Run with Docker Compose:**
    * From the project root directory (`SINGULARITYHEALTH/`), run:
        ```bash
        docker-compose up --build
        ```
    * The `--build` flag is only necessary the first time or if you make changes to `Dockerfile`s or dependencies. For subsequent runs, `docker-compose up` is usually sufficient.

4.  **Accessing the Application:**
    * **Frontend:** Open your browser and go to `http://localhost:3000`
    * **Backend (Django/GraphQL API):** Accessible at `http://localhost:8000`
        * GraphQL endpoint: `http://localhost:8000/graphql/`
        * Django Admin: `http://localhost:8000/admin/` (credentials will be what you set for `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD` in your `.env` file).

5.  **Stopping the Application:**
    * Press `Ctrl+C` in the terminal where `docker-compose up` is running.
    * To remove the containers, network, and volumes (use with caution if you want to preserve DB data):
        ```bash
        docker-compose down -v
        ```

---

## Running the Project Locally (Native Setup)

This method requires you to install and manage dependencies directly on your system.

### 1. Backend Setup (Django)

1.  **Navigate to the Backend Directory:**
    ```bash
    cd SINGULARITYHEALTH/backend
    ```

2.  **Create and Activate a Python Virtual Environment:**
    * Ensure Python 3.11 is your active Python version.
    * Create the virtual environment:
        ```bash
        python3.11 -m venv venv
        ```
    * Activate it:
        * On macOS/Linux: `source venv/bin/activate`
        * On Windows (Git Bash or WSL): `source venv/bin/activate`
        * On Windows (Command Prompt/PowerShell): `venv\Scripts\activate`

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up PostgreSQL Database:**
    * Install PostgreSQL server on your system if you haven't already.
    * Start the PostgreSQL service (commands vary by OS, e.g., `sudo service postgresql start` on some Linux distros, or it might start automatically on macOS/Windows).
    * Create a PostgreSQL database and a user for this project. For example, using `psql`:
        ```sql
        CREATE DATABASE singularity_db_local;
        CREATE USER your_local_user WITH PASSWORD 'your_local_password';
        ALTER ROLE your_local_user SET client_encoding TO 'utf8';
        ALTER ROLE your_local_user SET default_transaction_isolation TO 'read committed';
        ALTER ROLE your_local_user SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE singularity_db_local TO your_local_user;
        ```
        **Note:** Replace `singularity_db_local`, `your_local_user`, and `your_local_password` accordingly.

5.  **Set Up Backend Environment Variables:**
    * In the `SINGULARITYHEALTH/backend/` directory, find the `env.example.backend` file.
    * Copy it to a new file named `.env` (i.e., `SINGULARITYHEALTH/backend/.env`):
        ```bash
        cp env.example.backend .env
        ```
    * Open `SINGULARITYHEALTH/backend/.env` and update the `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` to match your local PostgreSQL setup. Also, set a unique `SECRET_KEY`.

6.  **Apply Database Migrations:**
    * Ensure your virtual environment is activated and you are in the `SINGULARITYHEALTH/backend/` directory.
    ```bash
    python manage.py migrate
    ```

7.  **Create a Superuser (Optional but Recommended):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create an admin user.

8.  **Run the Backend Development Server:**
    ```bash
    python manage.py runserver
    ```
    The backend will typically be available at `http://localhost:8000`.

### 2. Frontend Setup (React)

1.  **Navigate to the Frontend Directory:**
    * Open a new terminal window/tab.
    ```bash
    cd SINGULARITYHEALTH/frontend
    ```

2.  **Install Node.js Dependencies:**
    ```bash
    npm install
    ```

3.  **Run the Frontend Development Server:**
    ```bash
    npm start
    ```
    The frontend will typically be available at `http://localhost:3000`. It will connect to the backend running at `http://localhost:8000`.

---

## Testing

This project includes a comprehensive suite of automated tests to ensure the reliability and correctness of the backend application. The tests cover Django models, custom manager logic, and the GraphQL API (both mutations and queries).

### Test Suites Overview

The tests are organized into several classes, primarily focusing on:

1.  **`ModelUnitTests`**:
    * **Purpose**: Verifies the functionality of individual Django models such as `Country`, `TypeDocument`, `AppUser`, `UserDocument`, and `ContactInfo`.
    * **Coverage**: Includes tests for model creation, string representations (`__str__` method), and custom field validators (e.g., `phone_validator`, `address_validator` in `ContactInfo`).

2.  **`UserManagerUnitTests`**:
    * **Purpose**: Validates the custom `UserManager` for the `AppUser` model.
    * **Coverage**: Ensures correct behavior for creating regular users (e.g., requiring an email, normalizing email case) and superusers.

3.  **`GraphQLIntegrationTests`**:
    * **Purpose**: Tests the integration and functionality of GraphQL mutations. These tests interact with the GraphQL schema to simulate client requests for data modification.
    * **Coverage**:
        * `createCountry`: Verifies the creation of new `Country` objects.
        * `createTypeDocument`: Verifies the creation of new `TypeDocument` objects.
        * `registerUser` (Complete Flow): Tests the entire user registration process, including the creation of the `AppUser`, associated `UserDocument`, and `ContactInfo`.
        * Edge Cases: Includes tests for scenarios like attempting to register with an existing email and providing invalid data during registration (e.g., invalid email format, short password, incorrect foreign key IDs).

4.  **`GraphQLAPITests`**:
    * **Purpose**: Tests the integration and functionality of GraphQL queries. These tests interact with the GraphQL schema to simulate client requests for data retrieval.
    * **Coverage**:
        * `allCountries`: Verifies fetching a list of all countries.
        * `allDocumentTypes`: Verifies fetching a list of all document types.
        * `countryById`: Verifies fetching a specific country by its ID.
        * `documentTypeById`: Verifies fetching a specific document type by its ID.

### Running the Tests

You can run the tests using Django's `manage.py` command.


## Key Technologies

* **Backend:** Python, Django, Django REST framework, Graphene-Django (GraphQL), PostgreSQL
* **Frontend:** JavaScript, React, Apollo Client
* **Containerization:** Docker, Docker Compose