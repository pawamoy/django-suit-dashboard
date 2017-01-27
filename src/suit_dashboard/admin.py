
from hashlib import sha256

from .views import PartialResponse
from .widgets import RealTimeWidget

REALTIME_WIDGETS = []


def register_realtime(widget):
    if widget.url_name:
        url_name = widget.url_name
    else:
        url_name = widget.__name__

    if not hasattr(widget, 'get_updated_content'):
        raise AttributeError('Widget %s must implement get_updated_content '
                             'method.' % widget)
    elif not callable(widget.get_updated_content):
        raise ValueError('get_updated_content in widget %s is not callable'
                         % widget)

    if url_name in [w.url_name for w in REALTIME_WIDGETS]:
        raise ValueError('URL name %s is already used by another '
                         'real time widget.' % url_name)

    if widget.url_regex is None:
        url_regex = sha256(url_name.encode('utf-8'))
        url_regex = url_regex.hexdigest()[:32]
        url_regex = 'realtime/' + url_regex
    else:
        url_regex = widget.url_regex

    if url_regex in [w.url_regex for w in REALTIME_WIDGETS]:
        raise ValueError('URL regex %s is already used by another '
                         'real time widget.' % url_regex)

    if isinstance(widget, RealTimeWidget):
        def get_data(self):
            return widget.get_updated_content()
    elif isinstance(widget, type):
        def get_data(self):
            return widget().get_updated_content()

    class GeneratedView(PartialResponse):
        pass

    GeneratedView.get_data = get_data
    GeneratedView.url_name = url_name
    GeneratedView.url_regex = url_regex
    GeneratedView.refresh_time = widget.refresh_time

    REALTIME_WIDGETS.append(GeneratedView)
    return widget
