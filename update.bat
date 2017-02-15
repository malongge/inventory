echo "-------update server start-----------------------"
d:
cd d:\project\inventory\
git pull
pip install django-suit -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install django-braces -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
echo "----------update done------------------------"
