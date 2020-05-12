---
Github把django2.1.18给和谐了，requirements.txt里面改成了2.2.10，如果使用有问题的话，就换成2.1.18吧
---
## 安装环境
- 1.需要一个python3.6.5的环境
```python
1.执行安装脚本即可
sh install_python.sh

2.创建虚拟环境
mkvirtualenv yingops 

3.安装依赖文件
pip install -r requirements.txt
```
- 修改Django2YingOps/settings.py配置文件（主要是mysql的连接地址和webssh地址）
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '数据库名称',
        'USER': '数据库用户名',
        'PASSWORD': '数据库密码',
        'HOST': '数据库IP',
        'PORT': '3306',
    }
}
# webssh默认端口8000，在/assets/websshs/该页面可以启停webssh
WSSH_IP = 'webssh_ip:8000'
```
- 创建超级管理员及初始化数据库
```python
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
```
- 运行
```python
python manage.py runserver 0.0.0.0:8888
```
- 访问
```python
http://ip:8888
```

- 使用
```python
1.第一次使用时，需要在该界面执行初始化（新增资产信息界面） --> /assets/init/
2.使用远程webssh功能，需要到该页面进行启动webssh --> /assets/websshs/
3.后端页面url后缀为 --> /xadmin
```

- 注意事项
```python
1.如果安装mysqlclient时报错  可以使用pymysql在需要修改下面的文件
Django2YingOps/__init__.py 或者settings.py中加入
import pymysql
pymysql.install_as_MySQLdb()

2.服务器需要安装nmap(如果使用了install_python.sh，这一步可以省略)
yum install -y nmap

3.界面上所有的功能都会有，之前使用的python2进行开发的，现在改成python3，部分功能还未更新进去

4.前端页面是网上找的模板，AceAdmin，需要调样式可以自行下载

5.webssh是基于https://github.com/huashengdun/webssh，没有做二次开发，直接使用的
```
