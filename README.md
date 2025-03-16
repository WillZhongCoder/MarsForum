# MarsForum
This is a project about a forum with Flask.

### Getting Started

* This project is based on python 3.9.0, please do not use different version of python.

To start, install the project with `pip install -r requirements.txt` and then run `python app.py`

#### AI

With AI functions, download ollama and pull deepseek-r1:14b and deepseek-coder-v2

to pull run these commands:
```bash
ollama run deepseek-r1:14b
ollama run deepseek-coder-v2
```

#### Database

To get prepared of database, run 
```python
from app import create_app, db
with create_app().app_context():
		db.create_all()

```
in python console

#### Super User

To create a superuser, run app and register with username `admin` and password `YOUR PASSWORD`
and run this command in console:
```bash
sqlite3 instance/site.db
````
```sql
UPDATE user SET is_admin = 1 WHERE username = 'admin';
```

### Exploring

To explore the project, go to `http://127.0.0.1:5000/` or you can change the adress in `app.py`\
to open IPV6 address
change the address in `main.py` to `::`
like this:
```python
if __name__ == '__main__':
    app.run(host="::", port=8000)
```


