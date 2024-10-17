import subprocess
import sys

# Lista de paquetes a instalar
packages = [
    "asyncpg==0.27.0",
    "ormar==0.12.1",
    "fastapi",
    "uvicorn[standard]",
    "sqlalchemy",
    "typing",
    "pydantic",
    "pydantic-settings",
    "psycopg2-binary",
    "uuid6",
    "python-dotenv",
    "paho-mqtt",
    "requests",
    "fastapi_mail",
    "boto3",
    "flake8",
    "pyjwt",
    "bcrypt",
]


# Función para instalar paquetes
def install_packages(packages):
    for package in packages:
        print(f"Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# Ejecutar la instalación
if __name__ == "__main__":
    install_packages(packages)
