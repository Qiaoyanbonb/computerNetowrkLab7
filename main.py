import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

# 邮件内容
sender_email = "ustbqiaoyanbo@163.com"
receiver_email = "3498591250@qq.com"
password = "JAj5KRHUTXmk3p7t"  # 这里使用应用密码，如果有双重验证
subject = "蒋公中正"
message = "给你图了"

# 创建一个多部分邮件
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# 邮件正文
msg.attach(MIMEText(message, 'plain'))

attachment_path = "National Flag Anthem of the Republic of China.mp3"

# 检查文件是否存在
if os.path.exists(attachment_path):
    # 读取文件内容并添加到邮件中
    with open(attachment_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
    # 修改附件的头部信息
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
    msg.attach(part)
else:
    print(f"文件不存在: {attachment_path}")

# 发送邮件 - 使用SSL连接
try:
    server = smtplib.SMTP_SSL('smtp.163.com', 465)  # 使用SSL加密
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
    print("邮件发送成功")
except Exception as e:
    print(f"邮件发送失败: {e}")