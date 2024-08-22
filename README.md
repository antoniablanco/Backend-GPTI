# DestinAI

To run the program, you must install the dependencies first. To do this, run the following command in the terminal:

```bash
python packages.py
```

Then, you can run the program by running the following command in the terminal:

```bash
python main.py
```

# E-R


# Docker

To run docker, you must execute the following command from the directory where docker-compose.yml is located.

```
docker compose up -d
```

```
sudo docker volume rm name-volume
```

```
docker compose down
```

## Commands utils

```
sudo docker rm $(sudo docker ps -aq)
```

```console
sudo docker rmi $(sudo docker images -aq)
```

```console
sudo docker rmi $(sudo docker images -aq)
```

```
docker exec -it destinai-db-1 psql -U POSTGRES_USER -d POSTGRES_DB
```

# Sequelize commands

Start psql: `sudo service postgresql start` or `psql postgres`

Connect a bdd: `\c "nombre_bdd"`

Show all tables in a bdd: `\d`

Show all users: `\du`

Show al bdd: `\l`

Create a user: `sudo -u postgres createuser --superuser [INGRESAR_USUARIO]:`

Create bdd: `sudo -u postgres createdb [INGRESAR_NOMBRE_BDD]` or `CREATE DATABASE -name`

Eliminate bdd: `DROP DATABASE -name;`

Create password for a user: `ALTER USER [INGRESAR_USUARIO] WITH PASSWORD 'CLAVE_GENERICA';`

Connect to a bdd: `psql -U tu_usuario -d nombre_db`

Restart bdd: `DROP SCHEMA public CASCADE; CREATE SCHEMA public;`

Resetting IDs in Databases: `ALTER SEQUENCE name_seq RESTART WITH 1;`

# Arquitectura

Backend-GPTI/
|-- Api/
|   |-- models/
|   |-- routes/
|   |-- schemas/
|   |-- main.py
|   |-- packages.py
|   |-- database.py
|   |-- Dockerfile
|-- docker-compose.yml
|-- .env
|-- .gitignore

# .env

Must contain at list

* POSTGRES_USER = postgres_user
* POSTGRES_PASSWORD = postgres_password
* POSTGRES_DB = postgres_db_name
* DATABASE_URL= postgresql://username:password@db:5432/your_db_name
* PORT = 9000

# Generate seeds

```
docker exec -it /route/ npm run seed:run
```

# Linter Flake8

To maintain code integrity, `flake8` is used.

In the .flake8 file the rules are define, and also those rules that should be ignored.

```
flake8 .
```

# EC2
