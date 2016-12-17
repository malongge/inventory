echo "-------update server start-----------------------"
d:
cd d:\project\inventory\
git pull
pip uninstall django-searchable-select
pip uninstall django-selectable
python manage.py migrate
echo "----------update done------------------------"
