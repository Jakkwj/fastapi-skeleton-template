from fastapi.requests import Request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, Mail, To

from config.config import get_settings

settings = get_settings()


def send_mail_sendgrid(subject: str, to_email: str, username: str, url: str, template_id: str):
    """发送邮件.

    fastapi BackgroundTasks 发起的异步任务, 所以此发送邮件任务是异步的

    Email('noreply@your_email.org', 'your_user_name')  # 第二个参数为 邮件用户名 your_user_name

    使用 templates
    https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-templates

    Args:
        subject: 邮件主题
        to_email: 收件人邮箱
        html: 邮件 html 内容
    """
    sendgrid_client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    message = Mail(
        Email("noreply@your_email.org", "your_user_name"), To(to_email), subject, is_multiple=True
    )

    message.template_id = template_id
    message.dynamic_template_data = {"subject": subject, "username": username, "url": url}

    sendgrid_client.client.mail.send.post(request_body=message.get())  # type: ignore


async def send_confirm_mail(username: str, to_email: str, token: str, request: Request):
    """用户注册时发送确认邮件, token 默认有效期为 1 小时
    利用 redis 10s 内只发送一次邮件
    使用 sendgrid 的模版即可, 不需要自己设计
    """
    if not await request.app.redis.hget(name="send_confirm_mail", key="send_confirm_mail"):
        await request.app.redis.hset(
            name="send_confirm_mail", key="send_confirm_mail", value="send_confirm_mail"
        )

        subject = "Signup Confirmation"
        url = f"{settings.FRONTEND_URL}/sign/confirm/{token}/"
        send_mail_sendgrid(subject, to_email, username, url, settings.SENDGRID_TEMPLATE_ID_CONFIRM)

    await request.app.redis.expire(name="send_confirm_mail", time=10)  # 相当于 10s 内只发一次邮件
