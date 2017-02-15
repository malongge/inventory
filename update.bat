echo "-------update server start-----------------------"
d:
cd d:\project\inventory\
pip install django-suit
git pull
python manage.py migrate
echo "----------update done------------------------"
