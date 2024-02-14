from config.settings.base import *  # noqa
from config.settings.base import env

# GENERAL

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="qgk0jKApiWG9faJ5IRztKfxK2hjDgf2VnnYLHrRevavRDmU59GZD4BdPltGweVgd",
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHE

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("REDIS_URL", default="redis://localhost:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
