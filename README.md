#### 接收Nagios信息发送到微信端

[![Python3](https://img.shields.io/badge/Python-3.6+-blue.svg?style=popout&)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-1.1.1-orange.svg?style=popout&)](https://palletsprojects.com/p/flask/)

#### 机器要求
需要外网IP地址,端口必须是80


#### UWSGI配置
```ini
[uwsgi]
http = 0.0.0.0:80
#  项目代码路径
chdir = /srv/wx/nagios-weixin
#  python 安装路径
home = /usr/local/python3
wsgi-file = %(chdir)/web.py
callable = app
master = true
processes = 2
threads = 5
vacuum = true
pidfile = %(chdir)/wx_web.pid
daemonize = %(chdir)/wx_web.log
```
#### UWSIG 启停
```shell script
# cd /srv/wx/nagios-weixin
# /usr/local/python3/bin/uwsgi --ini config/uwsig.ini
# /usr/local/python3/bin/uwsgi --reload wx_web.pid
# /usr/local/python3/bin/uwsgi --stop wx_web.pid
```

#### 微信appID,appsecret配置
路径: conf/config.json
```json
{
  "app_id":"wx4fc565f7546opa-odaop9",  // appID
  "secret":"2864f4114f5ea4c7ccb1opiuaaw098" // appsecret
}
```

#### 微信回调接口
web.py 文件
```python
# 　配置微信回调接口秘钥
TOKEN = "1780ea515b9dc9bf"
# 修改12~13行 TOKEN 需要跟公众平台回调接口保持一致
```

####　绑定
绑定微信,扫描二维码关注公共号后,发送直接回复邮件地址,则可以绑定成功,一个邮件只能绑定一个微信号,一个微信号也只能绑定一个邮箱账号



#### 配置nagios
##### commands.cfg文件增加以下内容
```
define command{
    command_name wx_host_mail
    command_line /usr/bin/printf "%b" "主机报警: $HOSTNAME$ is $HOSTSTATE$\n通知类型: $NOTIFICATIONTYPE$\n主机: $HOSTALIAS$\n状态:$HOSTSTATE$\nIP地址: $HOSTADDRESS$\n时间: $LONGDATETIME$\n信息:\n$HOSTOUTPUT$\n" | /usr/local/python3/bin/python3 /srv/wx/nagios-weixin/send.py  --mail $CONTACTEMAIL$
}

define command{
    command_name wx_server_mail
    command_line /usr/bin/printf "%b" "服务报警: $HOSTNAME$ is $HOSTSTATE$\n通知类型: $NOTIFICATIONTYPE$\n服务: $SERVICEDESC$\n主机: $HOSTALIAS$\nIP地>址: $HOSTADDRESS$\n状态: $SERVICESTATE$\n时间: $LONGDATETIME$\n信息:\n$SERVICEOUTPUT$\n" | /usr/local/python3/bin/python3 /srv/wx/nagios-weixin/send.py  --mail $CONTACTEMAIL$
}
```

#### 消息发送测试
```shell script
# /usr/local/python3/bin/python3 send.py --help # 帮助信息
usage: send.py [-h] [--mail MAIL [MAIL ...]] [--content CONTENT] [--list]

微信消息发送工具

optional arguments:
  -h, --help            show this help message and exit
  --mail MAIL [MAIL ...], -m MAIL [MAIL ...]
                        邮箱地址
  --content CONTENT, -c CONTENT
                        消息内容
  --list, -l            列出绑定邮箱地址

# /usr/local/python3/bin/python3 send.py -l #　列出所有绑定用户
+------------------+----------+------------+
|       邮箱       | 微信昵称 |  创建时间  |
+------------------+----------+------------+
| 89411299sal@qq.com |    XY    | 1565370502 |
+------------------+----------+------------+

/usr/local/python3/bin/python3 send.py --mail 89411299sal@qq.com -c 这是一条测试警告 # 发送消息方法一
INFO:root:XY,邮箱为:89411299sal@qq.com发送消息成功...
echo "这是第二条测试警告" | /usr/local/python3/bin/python3 /srv/wx/nagios-weixin/send.py --mail 89411299sal@qq.com # 发送消息方法二
INFO:root:XY,邮箱为:89411299sal@qq.com发送消息成功...
```
