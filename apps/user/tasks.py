from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_register_email(register_url, email):
    message = '<h1>欢迎您成为<每日新鲜>注册用户！</h1>请点击下面的链接激活您的账户<br>' \
              '<a href="{register_url}">{register_url}</a>'.format(register_url=register_url)
    send_mail(
        subject="<每日新鲜>注册信息",
        message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        html_message=message
    )
