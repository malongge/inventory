echo "-------update server start-----------------------"
d:
cd d:\project\inventory\
pip install django-suit -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
git pull
python manage.py migrate
echo "----------update done------------------------"
