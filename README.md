#接受nagios 信息发送到微信端

###环境要求
工作环境要求 python3.4+

模块要求: flask,requests
安装方法: pip install flask
安装方法: pip install requests

###操作系统 Centos6.7 x86_64


###Python3.4.4安装
>

>
下载安装包
>
[root@centos6-test-1 nagios-weixin]# wget https://www.python.org/ftp/python/3.4.4/Python-3.4.4.tgz
>
编译安装
>
[root@centos6-test-1 nagios-weixin]tar zxf Python-3.4.4.tgz
>
[root@centos6-test-1 nagios-weixin]# cd Python-3.4.4
>
[root@centos6-test-1 Python-3.4.4]# ./configure --prefix=/usr/local/python3.4.4
>
[root@centos6-test-1 Python-3.4.4]# ./configure --prefix=/usr/local/python3.4.4
>
[root@centos6-test-1 Python-3.4.4]# make && make install
>
[root@centos6-test-1 Python-3.4.4]#ln -s /usr/local/python3.4.4 /usr/local/python3
>
[root@centos6-test-1 Python-3.4.4]#/usr/local/python3/bin/pip3 install flask
>
[root@centos6-test-1 Python-3.4.4]#/usr/local/python3/bin/pip3 install requests
>
###配置如下
1.
>
访问：http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login地址
用自己的微信账号扫码登录获取微信平台测试账号

2.
>
确保机器有外网IP
>
运行 webapp.py
>
webapp.py 一下操作需要用到,webapp.py默认使用的是80端口
>
	接口验证，微信端发送邮箱到webapp.py 收到消息后，存入数据供发送消息调用
>
	微信和邮箱绑定完成后，则可以关闭，发送消息不需要此程序
>
>
3.
>
配置接口信息
>
填写接口配置信息，此信息需要你有自己的服务器资源，填写的URL需要正确响应微信发送的Token验证
>
4.
>
添加模板信息
>
模板标题:故障通报通知
>
模板内容:
>
{{first.DATA}} 故障现象：{{performance.DATA}} 故障时间：{{time.DATA}} {{remark.DATA}}
>
5.
>
配置cofig/config.json文件
>
{
 "appid": "aaaaa",
>
 "secret": "aaaaa",
>
 "template_id":"6puShra9rwhBxNm12lQvFxoJbmKa_ONkemF4TV0",
>
 "smtp_server": "smtp.sina.com",
>
 "mail_sender": "aaa@sina.com",
>
 "mail_password": "aaaa"
>
}
>
###参数作用:
>
appid  开发者ID
>
secret 开发者密码
>
template 模板消息ID
>
>
如果邮箱没有绑定用户则使用下面参数邮件发送
>
smtp_server 邮件服务器地址
>
mail_sender  邮件账号
>
mail_password 邮件密码
>
配置cofig/token.json文件
>
{
>
  "token": "xiaoixn"
>
}
token 微信跟服务器,认证的密码
>

6.
>
测试使用
>
可以使用下面命令测试
>
 echo "test"|/usr/local/python3/bin/python3 app.py  -m aaa@sina.com -s test
>
方式结果:
>
    如果-m 后跟的邮箱地址,已经绑定微信则消息发送到微信端
>
    如果没有绑定则发送到邮箱
>
7.
>
绑定
>
绑定微信,扫描二维码关注公共号后,发送直接回复邮件地址,则可以绑定成功,一个邮件只能绑定一个微信号,一个微信号也只能绑定一个邮箱账号
>
8.配置nagios
>
commands.cfg文件增加以下内容
>
define command{
>
    command_name wx_host_mail
>
    command_line /usr/bin/printf "%b" "通知类型: $NOTIFICATIONTYPE$\n主机: $HOSTALIAS$\n状态:$HOSTSTATE$\nIP地址: $HOSTADDRESS$\n时间: $LONGDATETIME$\n信息:\n$HOSTOUTPUT$\n" | /usr/local/python3.4/bin/python3 /usr/local/nagios-weixin/app.py  -m $CONTACTEMAIL$ -s "主机报警: $HOSTNAME$ is $HOSTSTATE$"
>
}
>
define command{
>
    command_name wx_server_mail
>
    command_line /usr/bin/printf "%b" "通知类型: $NOTIFICATIONTYPE$\n服务: $SERVICEDESC$\n主机: $HOSTALIAS$\nIP地>址: $HOSTADDRESS$\n状态: $SERVICESTATE$\n时间: $LONGDATETIME$\n信息:\n$SERVICEOUTPUT$\n" | /usr/local/python3.4/bin/python3 /usr/local/nagios-weixin/app.py  -m $CONTACTEMAIL$ -s "服务报警: $HOSTNAME$ is $HOSTSTATE$"
>
}
>
