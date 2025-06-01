NovaHaus/
├── .env
├── .gitattributes
├── .gitignore
├── .python-version
├── .github/
│   └── CODEOWNERS
├── app.json
├── README_1.md
 - package.json (в корне проекта)
 - package-lock.json (в корне проекта)
├── manage.py
├── old-config.txt
├── Procfile
├── requirements.in
├── requirements.txt
├── README.md
├── robots.txt
├── test.txt
├── compress_images.py
├── locale/
│   ├── ru/
│   │   └── LC_MESSAGES/
│   │       ├── django.po  # Обновлён
│   │       └── django.mo
│   ├── en/
│   │   └── LC_MESSAGES/
│   │       ├── django.po  # Обновлён
│   │       └── django.mo
│   ├── de/
│   │   └── LC_MESSAGES/
│   │       ├── django.po  # Обновлён
│   │       └── django.mo
│   └── tr/
│       └── LC_MESSAGES/
│           ├── django.po  
│           └── django.mo
├── NovaHaus/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
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
│   ├── media/
│   │   └── hero-video.mp4
│   ├── css/
│   │   ├── pannellum.css
│   │   ├── panorama.css
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
│   │   └── styles.css
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
│   │   ├── compress_images.py
│   │   ├── panorama1.jpg
│   │   ├── background.jpg
│   │   ├── blog/
│   │   │   ├── post1.webp
│   │   │   ├── post2.webp
│   │   │   ├── post3.webp
│   │   │   ├── post1.jpg
│   │   │   ├── post2.jpg
│   │   │   └── post3.jpg
│   │   ├── favicon/
│   │   │   ├── android-chrome-192x192.png
│   │   │   ├── android-chrome-192x192.webp
│   │   │   ├── android-chrome-512x512.png
│   │   │   ├── android-chrome-512x512.webp
│   │   │   ├── apple-touch-icon.png
│   │   │   ├── apple-touch-icon.webp
│   │   │   ├── favicon.ico
│   │   │   ├── favicon-16x16.png
│   │   │   ├── favicon-16x16.webp
│   │   │   ├── favicon-32x32.png
│   │   │   ├── favicon-32x32.webp
│   │   │   ├── favicon-96x96.png
│   │   │   ├── favicon-96x96.webp
│   │   │   ├── favicon.svg
│   │   │   └── site.webmanifest
│   │   ├── icons/
│   │   │   ├── eco.png
│   │   │   ├── email.webp
│   │   │   ├── energy.png
│   │   │   ├── facade.webp
│   │   │   ├── facebook.webp
│   │   │   ├── house.webp
│   │   │   ├── instagram.webp
│   │   │   ├── leaf.png
│   │   │   ├── office.webp
│   │   │   ├── price.png
│   │   │   ├── quality.png
│   │   │   ├── recycle.png
│   │   │   ├── repair.webp
│   │   │   ├── telegram.webp
│   │   │   ├── time.png
│   │   │   ├── warehouse.webp
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
│   │   ├── icon-calculator.webp
│   │   ├── icon-info.png
│   │   ├── icon-info.webp
│   │   ├── logo.png
│   │   ├── logo.webp
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
│   │   ├── services/
│   │   │   ├── materials_cleaning.jpg
│   │   │   ├── renovation.jpg
│   │   │   ├── facade.jpg
│   │   │   ├── bathroom.jpg
│   │   │   ├── electrical.jpg
│   │   │   └── demolition.jpg
│   │   ├── slider/
│   │   │   ├── slide1.jpg
│   │   │   ├── slide2.jpg
│   │   │   └── slide3.jpg
│   │   └── team/
│   │       ├── member1.jpg
│   │       ├── member2.jpg
│   │       └── member3.jpg
│   ├── js/
│   │   ├── pannellum.js
│   │   ├── pannellum-custom.js
│   │   ├── testimonials.js
│   │   ├── 
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
│   │   ├── services.js
│   │   ├── slider.js
│   │   └── visualization.js
│   └── manifest.json
├── media/
│   ├── panoramas/
│   ├── portpolio/
│   └── services/
├── staticfiles/
└── templates/
    ├── base.html
    ├── errors/
    │   └── lockout.html
    └── includes/
        ├── footer.html  # Обновлён
        ├── header.html
        ├── modal.html
        └── slider.html  # ОбновлёнЫ

NovaHaus/eslint.config.js #в корне проекта
NovaHaus/main/templates/main/privacy.html
NovaHaus/static/models/sample_model.glb
NovaHaus/static/js/utils.js (новый файл)
static/images/placeholder.jpg

Добавь /main/templates/main/500.html
/static/images/favicon/favicon-192x192.png
static/js/three.min.js

NovaHaus/static/js/GLTFLoader.js



/static/models/ -- добавить всех этих файлов --
apartment_economy.glb, apartment_standard.glb, apartment_premium.glb
house_economy.glb, house_standard.glb, house_premium.glb
office_economy.glb, office_standard.glb, office_premium.glb
warehouse_economy.glb, warehouse_standard.glb, warehouse_premium.glb
facade_economy.glb, facade_standard.glb, facade_premium.glb
bathroom_economy.glb, bathroom_standard.glb, bathroom_premium.glb   ,  sample_model.glb

Новый файл static/js/main.js
static/images/favicon/favicon-192x192.png
static/css/visualization.css
