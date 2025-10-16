lms-backend/
│
├── config/                       # Main Django config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/                        # User management and roles
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── urls.py
│   ├── signals.py
│   └── tests.py
│
├── courses/                      # Course CRUD and content
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── enrollments/                  # Enrollment, progress tracking
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── payments/                     # Stripe integration
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── utils.py
│
├── core/                         # Shared helpers, middleware, utils
│   ├── utils.py
│   ├── permissions.py
│   ├── decorators.py
│   └── mixins.py
│
├── manage.py
├── .env
├── requirements.txt
└── README.md
