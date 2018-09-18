# Django pretty mails

Use Django template engine for html email sending.

## Getting Started

Package is on the beta version, so bugs may be occured :)

### Prerequisites

Tested on Django 2.1, but must work on Django 1.8 and higher


### Installing

Install via pip from [Github](https://github.com/vgaicuks/django-pretty-mails) repository

```
pip install git+https://github.com/vgaicuks/django-pretty-mails.git
```

add it to installed apps in django settings.py:

```python
INSTALLED_APPS = (
    'django_pretty_mails',
    ...
)
```

setup your settings:

```python
PRETTY_MAIL_TYPES = {
    'welcome': {
        'reply_to_mail': 'info@example.com',
        'subject': 'Welcome e-mail',
        'subject_prefix': '[Project] ',
        'admin_mails': ['admin@example.com'],
    },
}
```

send an e-mail:

```python
from django_pretty_mails import send_email

send_email('welcome', context, mails=['user@example.com'])

```



## Templates

Place your own design under 'templates/django_pretty_mails/base.html'.

### Overwritable blocks

Use Django {% block %} {% endblock %} tag:

#### Page title
```html
{% block page_title %}{% trans "Project | blah blah blah" %}{% endblock page_title %}

```

#### custom_css

```html
{% block custom_css %}
    <style>
    .head-wrap {
        background-color: #0062a8;
    }

    .head-wrap .content > table {
        background-color: #0062a8;
    }
    </style>
{% endblock custom_css %}

```

#### Logo and Brand name

```html
{% block brand_name %}
    <a href="{{ SITE_URL }}">
        {% trans "Brand name" %}
    </a>
{% endblock brand_name %}

{% block logo %}
    <a href="{{ SITE_URL }}">
        <img src="https://placehold.it/200x90/" title="Project" alt="Project">
    </a>
{% endblock logo %}

```

#### best_regards, socials_btns, contact_info and footer

```html
{% block best_regards %}
    <p>{% trans "Best Regards," %}<br>{% trans "Biosan team" %}</p>
{% endblock best_regards %}

{% block socials_btns %}
    <a href="#" class="soc-btn fb">{% trans "Facebook" %}</a>
    <a href="#" class="soc-btn tw">{% trans "Twitter" %}</a>
{% endblock socials_btns %}

{% block contact_info %}
    <p>
    {% trans "Email" %}:<strong><a href="mailto:info@example.com">mail@example.com</a></strong><br>
    {% trans "Web" %}: <strong><a href="{{ SITE_URL }}">example.com</a></strong><br>
    </p>
{% endblock contact_info %}

{% block footer %}{% endblock %}


```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
