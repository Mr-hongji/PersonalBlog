## **PersonalBlog**  个人博客
由于在平时在工作中一些知识点和学习笔记的记录以及一些网站的收藏都在（CSDN、看云文档、印象笔记）等，比较分散，不方便查看，所以才有了这个个人博客系统。

### **功能模块**
* 笔记

➣ 记录知识点和学习笔记
* 书签

➣ 用于收藏网页
* 文档

➣ 指定显示并浏览文件文件内容，可以把学习时做的项目例子等集中来方便温故知新
* 视频

➣ 整理平时的学习视频，可以随时观看，不用再把个视频拷贝来拷贝去的了，只要有网就可以观看

![image](https://github.com/Mr-hongji/MakePageTool/blob/master/images/perblog.png)


## **项目部署**
<br/>

### **部署方式**
* CentOs 7   nginx + uwsgi + django + sqlite3 + virtualenv + virtualenvwrapper + git

### **部署**
* 安装环境依赖
```linux
yum install gcc patch libffi-devel python-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel -y
```
* 安装 python3、 virtualenv 、virtualenvwrapper 、git 、sqlite3 、nginx、uwsgi

➣`wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz`
➣ `yum install -y sqlite   sqlite-devel`
➣ `yum install git`
➣ `pip3 install virtualenv `
➣ `pip3 install virtualenvwrapper `
➣ `wget  https://nginx.org/download/nginx-1.12.0.tar.gz`
➣ `pip3 install uwsgi (需要进入到virtualenv 虚拟环境中安装)`
详细安装：

 ➣ [python3、 virtualenv 、virtualenvwrapper]([Linux安装Python3](https://app.yinxiang.com/shard/s54/nl/19471276/1fce3bab-a630-4811-a124-3b2354750d7d))
➣ [nginx安装]([Linux安装Nginx](https://app.yinxiang.com/shard/s54/nl/19471276/11951e62-ef56-4337-a7c9-d6a80f528e72))


### **代码下载**
`git clone https://github.com/Mr-hongji/PersonalBlog.git`

### **安装依赖包**
* 在pyCharm导出依赖包文件
`pip3 install -r requirements.txt`

![image](https://github.com/Mr-hongji/MakePageTool/blob/master/images/requirements.png)

* 在发布环境中安装依赖

➣ 进入虚拟环境 
`workon venv1`
➣ 安装依赖
`pip3 install -r requirements.txt`

详细操作：[Python部署 确保环境一致性](https://app.yinxiang.com/shard/s54/nl/19471276/0578c4d3-0ace-495f-b2eb-44be41de4f56)
<br/>


### **Nginx 配置**
```
pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;
    upstream django {
        server 0.0.0.0:8000 weight=10;
    }

    server {
        listen      80;
        server_name  www.preblog.com;

        #charset koi8-r;

        access_log  logs/host.access.log  main;

        location / {
            include /opt/nginx1.12/conf/uwsgi_params;
            uwsgi_pass django;
            #root   /opt/html/;
            #index  myjd.html myjd.htm;            
        }

        #nginx处理静态资源配置 
        location /static {
            alias /opt/static/django;
        }

        #文档模块文件地址配置
        location /doc {
            alias /opt/files/docfile;
        }

        #视频块文件地址配置
        location /video {
            alias /opt/files/videofile;
        }

        error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }

```
















