from functools import wraps

from axes.handlers.proxy import AxesProxyHandler
from axes.helpers import get_lockout_response
from axes.request import AxesHttpRequest


def axes_dispatch(func):
    def inner(request: AxesHttpRequest, *args, **kwargs):
        if AxesProxyHandler.is_allowed(request):
            return func(request, *args, **kwargs)

        return get_lockout_response(request)

    return inner


def axes_form_invalid(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if AxesProxyHandler.is_allowed(self.request):
            return func(self, *args, **kwargs)

        return get_lockout_response(self.request)

    return inner
