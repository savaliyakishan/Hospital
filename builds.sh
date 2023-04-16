echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

echo "Building the project..."
python3.9 -m pip install -r requirements.txt

# echo "******************************************************************"

echo "Make Migration...1"
python3.9 manage.py makemigrations --noinput
echo "Make Migration...2"
python3.9 manage.py makemigrations hospital --noinput
echo "Make Migration...3"
python3.9 manage.py migrate --noinput

echo "###################################################################"
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell

python manage.py shell
from django.contrib.auth.models import User
user=User.objects.create_user('admin', password='admin')
user.is_superuser=True
user.is_staff=True
user.save()

echo "#################################dfasfdsdsf##################################"

python3.9 manage.py collectstatic --noinput
