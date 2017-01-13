from __future__ import unicode_literals

from functools import wraps
from hashlib import sha256
import datetime
import random

from .admin import register_realtime
from .views import PartialResponse
from .display import ParagraphDisplay, Display


class Widget(object):
    """Widget class."""
    html_id = None
    name = None
    content = None
    display = ParagraphDisplay()
    classes = ''

    def __init__(self, html_id=html_id, name=name, content=content,
                 display=display, classes=classes):
        """
        Init method.

        Args:
            html_id (str): an ID to set on the HTML item.
            name (str): the name of the item, displayed in HTML.
            content (): suitable content according to chosen display.
            display (Display): the type of display.
            classes (str): additional classes to pass to the HTML item.
        """
        if html_id != self.__class__.html_id:
            self.html_id = html_id
        if name != self.__class__.name:
            self.name = name
        if content != self.__class__.content:
            self.content = content
        if display != self.__class__.display:
            self.display = display
        if classes != self.__class__.classes    :
            self.classes = classes

    def get_html_id(self):
        return self.html_id

    def get_name(self):
        return self.name

    def get_content(self):
        return self.content

    def get_display(self):
        return self.display

    def get_classes(self):
        return self.classes


class RealTimeWidget(Widget):
    url_name = None
    url_regex = None
    refresh_time = 1000

    def __init__(self, *args, **kwargs):
        url_name = kwargs.pop('url_name', RealTimeWidget.url_name)
        url_regex = kwargs.pop('url_regex', RealTimeWidget.url_regex)
        refresh_time = kwargs.pop('refresh_time', RealTimeWidget.refresh_time)

        super(RealTimeWidget).__init__(*args, **kwargs)

        if url_name:
            self.url_name = url_name
        else:
            self.url_name = self.__class__.__name__

        if url_regex:
            self.url_regex = url_regex
        else:
            regex = sha256(self.url_name.encode('utf-8'))
            # regex = sha256(str(id(func)))  # Would just id be sufficient?
            regex = regex.hexdigest()[:32]
            while True:
                # regex = 'refreshable/' + ''.join(random.SystemRandom().choice(
                #     string.ascii_lowercase + string.digits) for _ in range(32))
                regex = 'refreshable/' + regex
                if regex not in [c.regex for c in PartialResponse.classes]:
                    self.url_regex = regex
                    break

        self.refresh_time = refresh_time


class CustomRealtimeWidget(RealTimeWidget):
    html_id = 'custom_widget'
    name = 'Custom Widget'
    display = Display(template='suit_dashboard/display/highcharts_custom.html')
    url_name = 'custom_rtw'
    url_regex = 'onsenfout123'

    # initial content
    def get_content(self):
        highcharts_dict = {
            'chart': {
                'type': 'spline',
                'marginRight': 10,
            },
            'title': {
                'text': 'Live random data'
            },
            'xAxis': {
                'type': 'datetime',
                'tickPixelInterval': 150
            },
            'yAxis': {
                'title': {
                    'text': 'Value'
                },
                'plotLines': [{
                    'value': 0,
                    'width': 1,
                    'color': '#808080'
                }]
            },
            'series': [{
                'name': 'Random data',
                'data': []
            }]
        }
        return highcharts_dict

    # get random points
    def get_updated_content(self):
        return (
            datetime.datetime.now(),
            random.choice(range(0, 25)),
        )


register_realtime(CustomRealtimeWidget)
