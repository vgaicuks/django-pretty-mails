from django.conf import settings
from django.core.mail import EmailMessage
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _, ugettext as __

from .app_settings import MAIL_TYPES


def send_email(mail_type, variables={}, subject=None, mails=None, attachments=[], admin_reply_to=None):
    """
    For each type you must create "{{ mail_type }}.html" template
    You can also create "{{ mail_type }}_admin.html" template.
    Then if "admin_mails" specified it will be used to send modified copy of mail,
    variables dict will be appended with "body" variable, which constains mail body

    reply_to_mail
    mails
    subject
    subject_prefix
    admin_mails
    admin_subject_prefix
    attachments - ['path_to_file', 'path_to_file_2']
    """

    if mail_type not in MAIL_TYPES:
        raise Exception('No such mail type in list!')

    mailconf = MAIL_TYPES[mail_type]

    if 'SITE_URL' not in variables:
        variables['SITE_URL'] = getattr(settings, 'SITE_URL', '/')

    body = render_to_string(f"django_pretty_mails/{mail_type}.html", variables)

    if not mails:
        if 'mails' in mailconf:
            mails = mailconf['mails']
        else:
            raise Exception('No mail to send to!')
    elif isinstance(mails, str):
        mails = [mails]

    if not subject:
        subject = _(mailconf['subject'])

    if 'subject_prefix' in mailconf and mailconf['subject_prefix']:
        subject = f"{__(mailconf['subject_prefix'])}{subject}"

    from_email = mailconf.get('from_email', settings.DEFAULT_FROM_EMAIL)
    reply_to_mail = mailconf.get('reply_to_mail', [])

    if isinstance(reply_to_mail, str):
        reply_to_mail = [reply_to_mail]

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        reply_to=reply_to_mail,
        to=mails
    )
    # attach files
    for attachment_path in attachments:
        email.attach_file(attachment_path)
    email.content_subtype = "html"
    email.send()

    if 'admin_mails' in mailconf:
        try:
            body = render_to_string(f"django_pretty_mails/{mail_type}_admin.html", {**variables, **{'body': body}})
        except TemplateDoesNotExist:
            pass

        if 'admin_subject_prefix' in mailconf:
            subject = f"{mailconf['admin_subject_prefix']}{subject}"

        # On case when MANAGES or ADMINS passed as admin_mails variable
        if isinstance(mailconf['admin_mails'], tuple):
            admin_mails = [r[1] for r in mailconf['admin_mails']]
        else:
            admin_mails = mailconf['admin_mails']

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            reply_to=admin_reply_to,
            to=admin_mails
        )

        # attach files
        for attachment_path in attachments:
            email.attach_file(attachment_path)
        email.content_subtype = "html"
        email.send()
