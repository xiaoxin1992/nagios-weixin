#  _*_ coding:utf-8
import smtplib
from email.mime.text import MIMEText
import socket
from wx_lib import log_write


class EasySendmail:
	def __init__(self, port=25):
		self.port = port

	@classmethod
	def setmail(cls, host, sender, passwd, mail_to, mail_sub, content):
		'''You must set attr:
		Host : mailServer exp: smtp.163.com
		Sender: mail from user
		Passwd: user passwd
		Mail_to: To user
		Mail_sub: mail subject
		content: message '''
		cls.host = host
		cls.sender = sender
		cls.passwd = passwd
		cls.mail_to = ';'.join(mail_to)
		cls.mail_sub = mail_sub
		cls.content = content

	@property
	def sendmail(self):
		'''sendmail: Start Connect server to send mail .'''
		self.message = """From: {0}
To: {1}
MIME-Version: 1.0
Content-type: text/plain
Subject: {2}

{3}
""".format(self.sender, self.mail_to, self.mail_sub, self.content)

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(10)
		try:
			s.connect((self.host, self.port))
			# print('Connect {0}:{1} successfuly !'.format(self.host, self.port))
		except Exception:
			print('Error: Can connect {0}:{1} !'.format(self.host, self.port))
			return False
		finally:
			if s:
				s.close()

		try:
			smtpobj = smtplib.SMTP(self.host, self.port)
			smtpobj.login(self.sender, self.passwd)
			smtpobj.sendmail(self.sender, self.mail_to, self.message.encode('GBK'))
			log_write.log("send mail to {0} ok".format(self.mail_to))
			smtpobj.quit()
		except smtplib.SMTPAuthenticationError as error:
			log_write.log(error)
			log_write.log('auth fail')
		except smtplib.SMTPException as error:
			log_write.log(error)
			log_write.log('Error: unable to send mail !')
		except Exception as e:
			log_write.log(e)
