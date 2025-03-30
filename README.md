NovaHaus/                     # Корневая папка проекта
├── locale/                   # Папка для файлов локализации
│   ├── ru/                   # Для русского
│   │   └── LC_MESSAGES/
│   │       ├── django.po     # Файл с переводами
│   │       └── django.mo     # Скомпилированный файл
│   ├── en/                   # Для английского
│   │   └── LC_MESSAGES/
│   │       ├── django.po
│   │       └── django.mo
│   └── de/                   # Для немецкого
│       └── LC_MESSAGES/
│           ├── django.po
│           └── django.mo
├
├── manage.py                 # Управляющий скрипт Django
├── NovaHaus/                 # Основная папка проекта (настройки)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main/                     # Приложение "main"
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py          # WebSocket consumers
│   ├── forms.py
│   ├── middleware.py
│   ├── models.py
│   ├── routing.py            # WebSocket routing
│   ├── tests.py
│   ├── translation.py
│   ├── views.py
│   ├── templates/
│   │   └── main/
│   │       ├── 3d_viewer.html
│   │       ├── about.html
│   │       ├── blog.html
│   │       ├── blog_post_detail.html
│   │       ├── calculator.html
│   │       ├── chatbot.html
│   │       ├── consultation.html
│   │       ├── contact.html
│   │       ├── dashboard.html
│   │       ├── faq.html
│   │       ├── home.html
│   │       ├── partner_success.html
│   │       ├── portfolio.html
│   │       ├── register.html
│   │       ├── register_partner.html
│   │       ├── reviews.html
│   │       └── services.html
├── static/                   # Статические файлы
│   ├── css/
│   │   ├── 3d-viewer.css
│   │   ├── buttons.css
│   │   ├── calculator.css
│   │   ├── cards.css
│   │   ├── chatbot.css
│   │   ├── footer.css
│   │   ├── forms.css
│   │   ├── global.css
│   │   ├── header.css
│   │   ├── media-queries.css
│   │   ├── partner.css
│   │   ├── reset.css
│   │   ├── services.css
│   │   ├── slider.css
│   │   └── visualization.css
│   ├── icons/
│   │   ├── email.png
│   │   ├── facade.png
│   │   ├── facebook.png
│   │   ├── house.png
│   │   ├── insulation.png
│   │   ├── instagram.png
│   │   ├── office.png
│   │   ├── repair.png
│   │   ├── telegram.png
│   │   ├── warehouse.png
│   │   └── ... [другие иконки]
│   ├── images/
│   │   ├── background.jpg
│   │   ├── blog/
│   │   ├── favicon/
│   │   ├── logo.png
│   │   ├── portfolio/
│   │   ├── slider/
│   │   └── team/
│   │       ├── member1.jpg
│   │       ├── member2.jpg
│   │       └── member3.jpg
│   ├── js/
│   │   ├── 3d-model.js
│   │   ├── ai-integration.js
│   │   ├── animations.js
│   │   ├── calculator.js
│   │   ├── chart.js
│   │   ├── chatbot.js
│   │   ├── email-integration.js
│   │   ├── feedback.js
│   │   ├── history.js
│   │   ├── language.js
│   │   ├── modal.js
│   │   ├── scripts.js
│   │   ├── service-worker.js
│   │   ├── slider.js
│   │   └── visualization.js
│   └── manifest.json
├── media/
├── templates/
├── staticfiles/
├── .env
├── .gitattributes
├── .gitignore
├── .python-version
├
├── old-config.txt
├── Procfile
├── requirements.in
├── requirements.txt
├── README.md
└── db.sqlite3