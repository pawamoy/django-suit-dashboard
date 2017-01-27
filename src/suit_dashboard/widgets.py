from __future__ import unicode_literals

from hashlib import sha256


class Widget(object):
    """Widget class."""
    html_id = None
    name = None
    content = None
    template = ''
    classes = ''

    def __init__(self, html_id=html_id, name=name, content=content,
                 template=template, classes=classes):
        """
        Init method.

        Args:
            html_id (str): an ID to set on the HTML item.
            name (str): the name of the item, displayed in HTML.
            content (): suitable content according to chosen display.
            display (Display): the type of display.
            classes (str): additional classes to pass to the HTML item.
        """
        if html_id != Widget.html_id:
            self.html_id = html_id
        if name != Widget.name:
            self.name = name
        if content != Widget.content:
            self.content = content
        if template != Widget.template:
            self.display = template
        if classes != Widget.classes:
            self.classes = classes

    def get_html_id(self):
        return self.html_id

    def get_name(self):
        return self.name

    def get_content(self):
        return self.content

    def get_template(self):
        return self.template

    def get_classes(self):
        return self.classes


class RealTimeWidget(Widget):
    url_name = None
    url_regex = None
    refresh_time = 1000

    def __init__(self, *args, **kwargs):
        url_name = kwargs.pop('url_name', self.__class__.url_name)
        url_regex = kwargs.pop('url_regex', self.__class__.url_regex)
        refresh_time = kwargs.pop('refresh_time', self.__class__.refresh_time)

        super().__init__(*args, **kwargs)

        if url_name:
            self.url_name = url_name
        else:
            self.url_name = self.__class__.__name__

        if url_regex is None:
            url_regex = sha256(url_name.encode('utf-8'))
            url_regex = url_regex.hexdigest()[:32]
            self.url_regex = 'realtime/' + url_regex
        else:
            self.url_regex = url_regex

        self.refresh_time = refresh_time
