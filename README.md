# Singularity Health User Registration API

Este proyecto implementa un API GraphQL para el registro de usuarios utilizando Django y Graphene-Django.

## Requisitos Previos

- Python 3.9+
- pip
- virtualenv (opcional, pero recomendado)

## Configuración del Entorno

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd singularity-health-backend
```

2. Crear y activar el entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Realizar migraciones:
```bash
python manage.py migrate
```

6. Ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Estructura del Proyecto

```
singularity-health-backend/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── manage.py
└── singularity/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── schema.py
    └── wsgi.py
└── users/
    ├── __init__.py
    ├── models.py
    ├── schema.py
    ├── mutations.py
    └── types.py
```

## API GraphQL

La API GraphQL está disponible en `/graphql/` y proporciona las siguientes operaciones:

- Mutation: registerUser
- Query: userProfile

## Tests

Para ejecutar los tests:
```bash
python manage.py test
```