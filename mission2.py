import poplib
from email.parser import Parser
from email.header import decode_header
import sys

# 连接到163的POP3服务器
pop_server = 'pop.163.com'
username = 'ustbqiaoyanbo@163.com'  # 例如：'user@163.com'
password = 'JAj5KRHUTXmk3p7t'  # 使用163邮箱的授权码作为密码

try:
    # 使用SSL连接
    pop_conn = poplib.POP3_SSL(pop_server)
except:
    # 如果SSL连接失败，尝试普通连接
    pop_conn = poplib.POP3(pop_server)

# 身份验证
pop_conn.user(username)
pop_conn.pass_(password)

# 获取邮件列表
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

# 拼接邮件内容，并确保解码字节为字符串
messages = [b'\n'.join(mssg[1]).decode('utf-8', errors='ignore') for mssg in messages]

# 解析邮件内容
parsed_messages = [Parser().parsestr(m) for m in messages]

# 函数用于解码邮件头信息
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

# 打印邮件信息
for msg in parsed_messages:
    print("From:", decode_str(msg['from']))
    print("To:", decode_str(msg['to']))
    print("Subject:", decode_str(msg['subject']))
    print("Date:", msg['date'])

    # 打印邮件正文
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode(errors='ignore')
            print("Body:", body)
            break

    print("\n" + "="*50 + "\n")

# 关闭连接
pop_conn.quit()

print("邮件接收和显示完成。")