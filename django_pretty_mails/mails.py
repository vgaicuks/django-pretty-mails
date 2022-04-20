from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _, ugettext as __

from .app_settings import MAIL_TYPES


def send_email(mail_type, variables={}, subject=None, mails=None, attachments=[], attachments_content=[],
               reply_to_mail=None, admin_reply_to=None, admin_mails=None, cc=None, bcc=None):
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
    attachments_content = [
        ('pdf_filename1.pdf', response.rendered_content, 'application/pdf'),
        ('pdf_filename2.pdf', response.rendered_content, 'application/pdf')
    ]
    """
    if mail_type not in MAIL_TYPES:
        raise Exception('No such mail type in list!')

    mailconf = MAIL_TYPES[mail_type]

    if 'SITE_URL' not in variables:
        variables['SITE_URL'] = getattr(settings, 'SITE_URL', '/')

    body_html, body_text = get_mail_body(mail_type, variables)

    if not mails:
        if 'mails' in mailconf:
            mails = mailconf['mails']
        else:
            raise Exception('No mail to send to!')

    f'{__(mailconf.get("subject_prefix", ""))}{subject or _(mailconf["subject"])}'

    from_email = mailconf.get('from_email', settings.DEFAULT_FROM_EMAIL)

    email = create_email_message(
        body_text,
        body_html,
        subject,
        convert_to_list(mails),
        from_email,
        attachments,
        attachments_content,
        convert_to_list(reply_to_mail or mailconf.get('reply_to_mail', [])),
        convert_to_list(cc or mailconf.get('cc', None)),
        convert_to_list(bcc or mailconf.get('bcc', None))
    )

    email.send()

    if 'admin_mails' in mailconf or admin_mails:
        try:
            body_html, body_text = get_mail_body(
                f'{mail_type}_admin', {
                    **variables,
                    'body': body_html
                })
        except Exception:
            pass

        subject = f"{mailconf.get('admin_subject_prefix', '')}{subject}"

        admin_mails = admin_mails or mailconf['admin_mails']

        # On case when MANAGES or ADMINS passed as admin_mails variable
        if isinstance(admin_mails, tuple):
            admin_mails = [r[1] for r in admin_mails]

        email = create_email_message(
            body_text,
            body_html,
            subject,
            admin_mails,
            from_email,
            attachments,
            attachments_content,
            admin_reply_to
        )

        email.send()


def convert_to_list(variable):
    if isinstance(variable, str):
        return [variable]
    return variable


def get_mail_body(template_name, variables):
    body_html = render_to_string(f"django_pretty_mails/{template_name}.html", variables)
    try:
        body_text = render_to_string(f"django_pretty_mails/{template_name}.txt", variables)
    except TemplateDoesNotExist:
        body_text = strip_tags(body_html)
    return body_html, body_text


def create_email_message(body_text, body_html, subject, mails, from_email, attachments=[], attachments_content=[],
                         reply_to_mail=None, cc=None, bcc=None):

    email = EmailMultiAlternatives(
        subject=subject,
        body=body_text,
        from_email=from_email,
        reply_to=reply_to_mail,
        to=mails,
        cc=cc,
        bcc=bcc
    )

    email.attach_alternative(body_html, 'text/html')

    # attach files
    for attachment_path in attachments:
        email.attach_file(attachment_path)

    for att in attachments_content:
        email.attach(*att)

    return email
