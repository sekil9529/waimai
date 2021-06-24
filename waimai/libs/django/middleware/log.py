# coding: utf-8

import os
import logging
import threading

from django.utils.deprecation import MiddlewareMixin

worker_local = threading.local()


class RequestLogMiddleware(MiddlewareMixin):
    """request日志中间件"""

    REAL_IP_KEY = 'HTTP_X_FORWARDED_FOR'

    def process_request(self, request):
        if self.REAL_IP_KEY in request.META:
            ip = request.META[self.REAL_IP_KEY]
        else:
            ip = request.META['REMOTE_ADDR']
        worker_local.ip = ip
        worker_local.path = request.get_full_path()
        worker_local.method = request.method


class RequestLogFilter(logging.Filter):
    """request日志过滤器"""

    def filter(self, record):
        record.ip = getattr(worker_local, 'ip', '')
        record.path = getattr(worker_local, 'path', '')
        record.method = getattr(worker_local, 'method', '')
        return True


def get_log_config(base_dir: str, version: int = 1, is_pro: bool = False):
    """获取日志配置

    :param base_dir: 基本路径
    :param version: 版本
    :param is_pro: 是否正式
    :return: dict
    """
    log_dir = os.path.join(base_dir, 'logs')
    handlers = ['all', 'error'] if is_pro else ['console']
    config = {
        'version': version,
        'disable_existing_loggers': True,
        'filters': {
            'standard': {
                '()': 'libs.django.middleware.log.RequestLogFilter'
            }
        },
        'formatters': {
            'standard': {
                'format': '[%(asctime)s.%(msecs)0.3d] - [%(levelname)s] - [%(ip)s] - [%(method)s] - [%(path)s] - '
                          '[%(name)s:%(lineno)d] - [%(threadName)s:%(thread)d] - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '[%(asctime)s.%(msecs)0.3d] - [%(levelname)s] - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'all': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir, 'all.log'),
                'mode': 'w+',
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
                'encoding': 'utf-8',
                'formatter': 'standard',
                'filters': ['standard'],
            },
            'error': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir, 'error.log'),
                'mode': 'w+',
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
                'encoding': 'utf-8',
                'formatter': 'standard',
                'filters': ['standard'],
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'filters': ['standard']
            },
            'simple': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            }
        },
        'loggers': {
            '': {
                'handlers': handlers,
                'level': 'INFO',
                'propagate': False
            },
            'django': {
                'handlers': ['simple'],
                'level': 'INFO',
                'propagate': False
            },
            'django.request': {
                'handlers': handlers,
                'level': 'INFO',
                'propagate': False
            },
            'django.server': {
                'handlers': handlers,
                'level': 'INFO',
                'propagate': False,
            }
        }
    }
    return config
