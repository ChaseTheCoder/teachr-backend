
Run locally
# teachr-backend python manage.py runserver

Add new app
1. python manage.py startapp {name}
2. add to INSTALLED_APPS in settings.py

Pull down
1. python3 -m venv {env name}  (i use 'env' for env name)
2. source env/bin/activate  (this activates your virual environment)
3. pip install -r requirements.txt  (downloads all your requirements)
4. python3 manage.py runserver (runs it locally within your virtual environment)
5. deactivate (dactivates your virual environment if you need a new one)