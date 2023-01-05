### 环境准备
- 安装python3以及pip
```
yum install python3 python3-pip -y
pip3 install -r requirement.txt
```
- 安装mysql
> 为了简单，本地直接运行docker
```
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mypassword -d mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

### 服务初始化
- 拉取代码并且进行初始化
```
git clone https://github.com/linwiker/pbms
cd pbms
pip3 install -r requirement.txt
python3 manage.py migrate
python3 manage.py makemigrations book
python3 manage.py migrate book
```

### 服务运行
```
python3 manage.py runserver 0.0.0.0:8000
```