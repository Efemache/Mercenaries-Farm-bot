from urllib import request, parse, error

from .settings import settings_dict

import logging

log = logging.getLogger(__name__)

def send_notification(message: dict):
    """Send notification message to a webhook url from `notificationURL` config."""
    if not settings_dict['notificationurl']:
        return
    url = settings_dict['notificationurl']
    try:
        data = parse.urlencode(message).encode()
        req = request.Request(url, data, method="POST")
        request.urlopen(req)
        log.info(f"notification sent: {message}")
    except error.HTTPError as e:
        log.error(f"notification HTTP error: {e.code}")
    except error.URLError as e:
        log.error(f"notification URL error: {e.reason}")
    except Exception as e:
        log.error(f"notification error: {e}")
