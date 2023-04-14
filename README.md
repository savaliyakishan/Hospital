Python version == 3.10.7

**  most important thing befor the run project fill the details in your .env file


1. craete env  
   python3.10 -m venv env

2. activate env 
   env\scripts\activete

3. install all reqirements from  requirements.txt 
   pip install -r requirements.txt

4. create migrations file using 
   python manage.py makemigrations or python manage.py makemigrations hospital

5. create database table
   python manage.py migrate

6. runserver
   python manage.py runserver

7. run this command on browser
   http://127.0.0.1:8000/login
