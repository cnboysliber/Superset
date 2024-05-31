# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#
import logging
import os
from datetime import timedelta
from typing import Optional

from celery.schedules import crontab
# from flask_appbuilder.security.manager import AUTH_OID, \
#     AUTH_REMOTE_USER, AUTH_DB, AUTH_LDAP, AUTH_OAUTH

basedir = os.path.abspath(os.path.dirname(__file__))

logger = logging.getLogger()


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)


# AUTH_TYPE = AUTH_OAUTH
# AUTH_USER_REGISTRATION = True
# FAB_PASSWORD_COMPLEXITY_ENABLED = True
# AUTH_USER_REGISTRATION_ROLE = "Admin"
# OAUTH_PROVIDERS = [
#     {
#         'name': 'google',
#         'whitelist': ['@shopee.com'],
#         'icon': 'fa-google',
#         'token_key': 'access_token',
#         'remote_app': {
#             'base_url': 'https://www.googleapis.com/oauth2/v2/',
#             'request_token_params': {
#                 'scope': 'email profile'
#             },
#             'request_token_url': None,
#             'access_token_url':
#                 'https://accounts.google.com/o/oauth2/token',
#             'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
#             'consumer_key': '129432723814-6juqap8rf7npkrfcf58h5463aejb53h5.apps.googleusercontent.com',
#             'consumer_secret': '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'
#         }
#     }
# ]

DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
DATABASE_USER = get_env_variable("DATABASE_USER")
DATABASE_PASSWORD = get_env_variable("DATABASE_PASSWORD")
DATABASE_HOST = get_env_variable("DATABASE_HOST")
DATABASE_PORT = get_env_variable("DATABASE_PORT")
DATABASE_DB = get_env_variable("DATABASE_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")
REDIS_CELERY_DB = get_env_variable("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = get_env_variable("REDIS_RESULTS_DB", "1")

# RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "SupersetMetastoreCache",
    "EXPLORE_FORM_DATA_CACHE_CONFIG": "RedisCache",
    "CACHE_KEY_PREFIX": "superset_results",
    # make sure this string is unique to avoid collisions
    "CACHE_DEFAULT_TIMEOUT": 86400,  # 60 seconds * 60 minutes * 24 hours
}

FILTER_STATE_CACHE_CONFIG = {
    "CACHE_TYPE": "SupersetMetastoreCache",
    "EXPLORE_FORM_DATA_CACHE_CONFIG": "RedisCache",
    "CACHE_KEY_PREFIX": "superset_filter",
    # make sure this string is unique to avoid collisions
    "CACHE_DEFAULT_TIMEOUT": 86400,  # 60 seconds * 60 minutes * 24 hours
}
EXPLORE_FORM_DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "SupersetMetastoreCache",
    "EXPLORE_FORM_DATA_CACHE_CONFIG": "RedisCache",
    "CACHE_KEY_PREFIX": "explore_data",
    # make sure this string is unique to avoid collisions
    "CACHE_DEFAULT_TIMEOUT": 86400,  # 60 seconds * 60 minutes * 24 hours
}


class CeleryConfig(object):
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = ("superset.sql_lab", "superset.tasks")
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_log_level = "DEBUG"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "email_reports.schedule_hourly": {
            "task": "email_reports.schedule_hourly",
            "schedule": crontab(minute=1, hour="*"),
        },
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ENABLE_EXPLORE_DRAG_AND_DROP": True,
    "ENABLE_DND_WITH_CLICK_UX": True,
}
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
WEBDRIVER_BASEURL = "http://superset:8088/"
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

SQLLAB_CTAS_NO_LIMIT = True

SMTP_HOST = "smtp.gmail.com"  # change to your host
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = "chengbo.li@shopee.com"
SMTP_PORT = 0  # your port eg. 587
SMTP_PASSWORD = "ajzvfjjblnmcsvar"
SMTP_MAIL_FROM = "chengbo.li@shopee.com"

# EMAIL_REPORT_FROM_ADDRESS = "1558723461@qq.com"
EMAIL_REPORT_BCC_ADDRESS = None

# security config
PUBLIC_ROLE_LIKE_GAMMA = True
PUBLIC_ROLE_LIKE = 'Gamma'
SESSION_COOKIE_SAMESITE = None

HTTP_HEADERS = {}
WTF_CSRF_ENABLED = False

# WebDriver configuration
# If you use Firefox, you can stick with default values
# If you use Chrome, then add the following WEBDRIVER_TYPE and WEBDRIVER_OPTION_ARGS
EMAIL_REPORTS_WEBDRIVER = "geckodriver"
WEBDRIVER_TYPE = "firefox"
WEBDRIVER_OPTION_ARGS = [
    "--force-device-scale-factor=2.0",
    "--high-dpi-support=2.0",
    "--headless",
]

# PREVIOUS_SECRET_KEY = 'qAfhTM9nKrEmiL/NGjP9PAeY/GXoru8drLb4T6zaWrOyNLbygZfBe2Ud'
# To find out 'CURRENT_SECRET_KEY' follow these steps
# 1. Got to superset shell : $ superset shell
# 2. Run the command       : >>> from flask import current_app; print(current_app.config["SECRET_KEY"])

SECRET_KEY = 'qAfhTM9nKrEmiL/NGjP9PAeY/GXoru8drLb4T6zaWrOyNLbygZfBe2Ud'
CONTENT_SECURITY_POLICY_WARNING = False
# Generate a secure SECRET_KEY usng "openssl rand -base64 42"
#
# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overridden
#
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(
        f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")
