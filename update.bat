echo "-------update server start-----------------------"
d:
cd d:\project\inventory\
git pull
python manage.py migrate
echo "----------update done------------------------"
