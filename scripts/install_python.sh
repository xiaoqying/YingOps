
```bash
#!/bin/bash
tools="git zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel net-tools wget "
yum -y install $tools
echo -e "\033[34m ----------1.安装完依赖包---------- \033[0m" 
py_version="3.6.5"
src_dir="/usr/local/src"
wget -P $src_dir https://www.python.org/ftp/python/$py_version/Python-$py_version.tgz
echo -e "\033[34m ----------2.下载完python安装包---------- \033[0m" 
mkdir -p /usr/local/python$py_version
cd $src_dir
tar -zxf Python-$py_version.tgz
cd $src_dir/Python-$py_version
./configure --prefix=/usr/local/python$py_version
make -j8 && make install -j8
echo -e "\033[34m ----------3.安装完python---------- \033[0m" 
ln -s /usr/local/python$py_version/bin/python3 /usr/bin/python3

cat >> ~/.bash_profile <EOF
PATH=$PATH:$HOME/bin:/usr/local/python${py_version}/bin
export PATH
EOF

source ~/.bash_profile

python3 -V
pip3 -V
echo -e "\033[34m ----------4.结束安装---------- \033[0m" 

mkdir ~/.pip
touch ~/.pip/pip.conf

cat >~/.pip/pip.conf<<EOF
[global]
index-url = https://pypi.douban.com/simple
EOF

pip3 install virtualenv
pip3 install virtualenvwrapper
mkdir ~/.Envs

cat >>~/.bashrc<<EOF
export WORKON_HOME=~/.Envs
export VIRTUALENVWRAPPER_PYTHON=/usr/local/python${py_version}/bin/python3
source /usr/local/python${py_version}/bin/virtualenvwrapper.sh
EOF
```
