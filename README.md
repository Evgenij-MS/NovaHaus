NovaHaus/
├── locale/
│   ├── ru/
│   │   └── LC_MESSAGES/
│   │       ├── django.po  # Обновлён
│   │       └── django.mo
│   ├── en/
│   │   └── LC_MESSAGES/
│   │       ├── django.po  # Обновлён
│   │       └── django.mo
│   └── de/
│       └── LC_MESSAGES/
│           ├── django.po  # Обновлён
│           └── django.mo
├── manage.py
├── NovaHaus/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── forms.py
│   ├── main.py
│   ├── middleware.py
│   ├── models.py
│   ├── routing.py
│   ├── tests.py
│   ├── translation.py
│   ├── views.py
│   └── templates/
│       └── main/
│           ├── 3d_viewer.html
│           ├── 404.html
│           ├── about.html
│           ├── blog.html
│           ├── blog_post_detail.html
│           ├── calculator.html
│           ├── chatbot.html
│           ├── consultation.html
│           ├── contact.html
│           ├── dashboard.html
│           ├── faq.html
│           ├── home.html
│           ├── partner_success.html
│           ├── portfolio.html
│           ├── register.html
│           ├── register_partner.html
│           ├── reviews.html
│           └── services.html  # Обновлён
├── static/
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
│   │   ├── services.css  # Обновлён (был пустой)
│   │   ├── slider.css
│   │   └── visualization.css
│   ├── fontawesome/
│   │   ├── css/
│   │   │   └── all.min.css
│   │   ├── js/
│   │   │   └── all.min.js
│   │   └── webfonts/
│   │       ├── fa-brands-400.ttf
│   │       ├── fa-brands-400.woff2
│   │       ├── fa-regular-400.ttf
│   │       ├── fa-regular-400.woff2
│   │       ├── fa-solid-900.ttf
│   │       ├── fa-solid-900.woff2
│   │       ├── fa-v4compatibility.ttf
│   │       └── fa-v4compatibility.woff2
│   ├── images/
│   │   ├── background.jpg
│   │   ├── blog/
│   │   │   ├── post1.jpg
│   │   │   ├── post2.jpg
│   │   │   └── post3.jpg
│   │   ├── favicon/
│   │   │   ├── android-chrome-192x192.png
│   │   │   ├── android-chrome-512x512.png
│   │   │   ├── apple-touch-icon.png
│   │   │   ├── favicon.ico
│   │   │   ├── favicon-16x16.png
│   │   │   ├── favicon-32x32.png
│   │   │   ├── favicon-96x96.png
│   │   │   ├── favicon.svg
│   │   │   └── site.webmanifest
│   │   ├── icons/
│   │   │   ├── email.png
│   │   │   ├── facade.png
│   │   │   ├── facebook.png
│   │   │   ├── house.png
│   │   │   ├── instagram.png
│   │   │   ├── insulation.png
│   │   │   ├── office.png
│   │   │   ├── repair.png
│   │   │   ├── telegram.png
│   │   │   └── warehouse.png
│   │   ├── icon-calculator.png
│   │   ├── icon-info.png
│   │   ├── logo.png
│   │   ├── portfolio/
│   │   │   ├── project1.jpg
│   │   │   ├── project1-large.jpg
│   │   │   ├── project1-small.jpg
│   │   │   ├── project2.jpg
│   │   │   ├── project2-large.jpg
│   │   │   ├── project2-small.jpg
│   │   │   ├── project3.jpg
│   │   │   ├── project3-large.jpg
│   │   │   └── project3-small.jpg
│   │   ├── services/  # Новая папка еще один файл в этой папке materials_cleaning.jpg
│   │   │   ├── renovation.jpg  # Новое
│   │   │   ├── facade.jpg  # Новое
│   │   │   ├── bathroom.jpg  # Новое
│   │   │   ├── electrical.jpg  # Новое
│   │   │   └── demolition.jpg  # Новое
│   │   ├── slider/
│   │   │   ├── slide1.jpg
│   │   │   ├── slide2.jpg
│   │   │   └── slide3.jpg
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
│   │   ├── services.js  # Новый
│   │   ├── slider.js
│   │   └── visualization.js
│   └── manifest.json
├── media/
│   ├── portpolio/
│   └── services/
├── templates/
│   ├── base.html
│   ├── errors/
│   │   └── lockout.html
│   └── includes/
│       ├── footer.html  # Обновлён
│       ├── header.html
│       ├── modal.html
│       └── slider.html  # Обновлён
├── staticfiles/
├── .env
├── .gitattributes
├── .gitignore
├── .python-version
├── app.json
├── old-config.txt
├── Procfile
├── requirements.in
├── requirements.txt
├── README.md
└── db.sqlite3

static/js/pannellum-custom.js (новый файл):
static/css/pannellum.css    (новый файл)