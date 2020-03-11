# shortlink
Short-link service with usage analytics

## Installation
1. Create virtual environment `python3.8 -m venv env`
2. Activate virtual environment `source env/bin/activate`
3. Install all requirements `pip install -r requirements`
4. Create database and grant all privileges for <username>
```
psql
CREATE DATABASE shortlink;
GRANT ALL PRIVILEGES ON DATABASE shortlink TO <username>;
```
 5. Update your db configuration in `config/config.txt`
 6. Run migrations `./manage.py migrate`
 7. Run django development server `./manage.py runserver 0.0.0.0:8000`
