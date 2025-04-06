NovaHaus/
├── locale/
│   ├── ru/LC_MESSAGES/{django.po,django.mo}
│   ├── en/LC_MESSAGES/{django.po,django.mo}
│   └── de/LC_MESSAGES/{django.po,django.mo}
├── manage.py
├── NovaHaus/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│   └── templates/           # Новое расположение base.html
│       └── base.html        # Главный шаблон перенесён сюда
├── main/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── forms.py
│   ├── middleware.py
│   ├── models.py
│   ├── routing.py
│   ├── tests.py
│   ├── translation.py
│   ├── views.py
│   └── templates/main/
│       ├── 3d_viewer.html
│       ├── about.html
│       ├── blog.html
│       ├── [...остальные шаблоны...]
│       └── services.html
├── static/
│   ├── fontawesome/         # Все новые файлы Font Awesome
│   │   ├── css/all.min.css
│   │   ├── js/all.min.js
│   │   └── webfonts/
│   │       ├── fa-brands-400.ttf
│   │       ├── fa-brands-400.woff2
│   │       ├── fa-regular-400.ttf
│   │       ├── fa-regular-400.woff2
│   │       ├── fa-solid-900.ttf
│   │       ├── fa-solid-900.woff2
│   │       ├── fa-v4compatibility.ttf
│   │       └── fa-v4compatibility.woff2
│   ├── css/[все ваши CSS-файлы]
│   ├── icons/[все иконки]
│   ├── images/[все изображения]
│   └── js/[все JS-файлы]
├── media/
├── staticfiles/
├── .env
├── .gitattributes
├── .gitignore
├── .python-version
├── old-config.txt
├── Procfile
├── requirements.in
├── requirements.txt
├── README.md
└── db.sqlite3