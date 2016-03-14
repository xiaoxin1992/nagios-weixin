#接受nagios 信息发送到微信端

###环境要求
工作环境要求 python3.4+

模块要求: flask
安装方法: pip install flask


###配置如下
1.
>
访问：http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login地址
用自己的微信账号扫码登录获取微信平台测试账号

2.
>
确保机器有外网IP
>
运行 wxweb.py
>
wxweb.py 一下操作需要用到
>
	接口验证，微信端发送邮箱到wxweb.py 收到消息后，存入数据供发送消息调用
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

6.
>
测试使用
>
可以使用下面命令测试
>
 python nagiosweixin.py  -m aaa@sina.com -s test -c "test ok"
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
