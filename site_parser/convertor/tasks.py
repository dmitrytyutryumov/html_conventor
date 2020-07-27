import os
import re
import typing
import uuid

import pdfkit
from celery.task import task
from decouple import config
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .models import ConvertorData


@task(name="convert_html_to_pdf")
def convert_html_to_pdf(pk: int) -> None:
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)
    file_name = f'{str(uuid.uuid4())}.pdf'
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    entity = ConvertorData.objects.get(pk=pk)
    subject = ''
    message = ''
    try:
        if entity.is_url:
            pdfkit.from_url(entity.source, file_path)
        else:
            content = entity.source
            if entity.domain:
                content = __prepare_html(entity.domain, entity.source)
            pdfkit.from_string(content, file_path)

        subject = 'Converting is finished'
        entity.output.name = file_name
        entity.save()
    except Exception as e:
        subject = 'Converting is failed. Please try again.'
        message = 'Try to resolve relative path to css/js/ico ' \
                  'files or provide domain with file.'
        if not entity.is_url:
            message = '\n'.join([message, str(e)])
    finally:
        send_email_task(
            subject=subject,
            message=message,
            recipient_list=[entity.email],
            attachments=[
                (entity.output.name, entity.output.read(), 'application/pdf')
            ] if entity.output else []
        )
    return


@task(name='send_email')
def send_email_task(
        subject: str, message: str, recipient_list: typing.List[str],
        attachments: typing.List[str] = None
):
    attachments = list(filter(None, attachments))
    email = EmailMultiAlternatives(
        subject=subject.capitalize(),
        body=message.capitalize(),
        from_email=config('EMAIL_HOST_USER'),
        to=recipient_list
    )

    [
        email.attach(*attachment) for attachment in attachments
    ]
    email.send(fail_silently=False)


def __prepare_html(domain: str, content: str) -> str:
    links = re.findall('[href|src]="([/.a-z0-9\-]+\.[a-z]+)"', content)
    for link in links:
        content = content.replace(
            link, os.path.join(domain, link.replace('../', '')))
    return content

