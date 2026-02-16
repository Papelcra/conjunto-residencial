# Gestión de Conjunto Residencial

Plataforma web para administración de conjuntos residenciales (Django + Python + PostgreSQL/SQLite).

## Funcionalidades principales
- Autenticación y roles: Administrador, Seguridad, Residente
- Gestión de apartamentos (CRUD)
- Notificación de pagos y control de morosidad
- Reservas de zonas comunes (próximamente)
- PQRS y anuncios

## Instalación
1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar: `.\venv\Scripts\activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Migraciones: `py manage.py migrate`
6. Crear superusuario: `py manage.py createsuperuser`
7. Correr servidor: `py manage.py runserver`

## Equipo
- Julian
- Javier
- Sara
- Jhandris
