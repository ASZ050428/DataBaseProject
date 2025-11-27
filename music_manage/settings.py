"""
Django settings for music_manage_system_backend project.
"""

from pathlib import Path
import os
import yaml

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 读取配置文件（统一使用 config 变量名）
with open(os.path.join(BASE_DIR, 'config.yaml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)  # 变量名统一为 config


# 安全设置
SECRET_KEY = config["DjangoSecretKey"]
DEBUG = config['Debug']
ALLOWED_HOSTS = ['*']
HOSTNAME = ALLOWED_HOSTS[0]

from datetime import timedelta
# JWT 配置
SIMPLE_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
    ),
    'TOKEN_lifetime': {
        'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    }
}

# 应用配置
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'UserManage',
    'ArtistManage',
    'AlbumManage',
    'SongManage',
    'CommentManage',
    'CollectionManage',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'music_manage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'music_manage.wsgi.application'


# 数据库配置（解决端口类型问题）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config['TaurusDBName'],
        'USER': config['TaurusDBUser'],
        'PASSWORD': config['TaurusDBPassword'],
        'HOST': config['TaurusDBHost'],
        'PORT': '3306',  # 关键修复：将整数转为字符串
        'OPTIONS': {
            'charset': 'utf8mb4',
            'connect_timeout': 10,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# 国际化
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# 静态文件
STATIC_URL = '/static/'


# Redis缓存配置（修正变量名）
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config['RedisAddress']}/{config['RedisDatabase']}",  # 使用 f-string 更简洁
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": config["RedisPassword"]
        }
    }
}