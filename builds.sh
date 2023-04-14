echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "******************************************************************"
python3.9 manage.py createsuperuser
admin
admin
admin
y
echo "Make Migration...1"
python3.9 manage.py makemigrations --noinput
echo "Make Migration...2"
python3.9 manage.py makemigrations hospital --noinput
echo "Make Migration...3"
python3.9 manage.py migrate --noinput

echo "###################################################################"
python3.9 manage.py collectstatic --noinput
