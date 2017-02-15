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


# import random
# from suit_dashboard.widgets import RealTimeWidget
# from suit_dashboard.admin import register_realtime
#
#
# class CustomRealtimeWidget(RealTimeWidget):
#     html_id = 'custom_widget'
#     name = 'Custom Widget'
#     template = 'app/dashboard/display/highcharts_custom.html'
#     url_name = 'custom_rtw'
#     url_regex = 'realtime/custom_rtw'
#     max_points = 30
#     refresh_time = 1000
#
#     # initial content
#     def get_content(self):
#         highcharts_dict = {
#             'chart': {
#                 'type': 'spline',
#                 'marginRight': 10,
#             },
#             'title': {
#                 'text': 'Live random data'
#             },
#             'xAxis': {
#                 'type': 'datetime',
#                 'tickPixelInterval': 150
#             },
#             'yAxis': {
#                 'title': {
#                     'text': 'Value'
#                 },
#                 'plotLines': [{
#                     'value': 0,
#                     'width': 1,
#                     'color': '#808080'
#                 }]
#             },
#             'series': [{
#                 'name': 'Random data',
#                 'data': []
#             }]
#         }
#         return highcharts_dict
#
#     # get random points
#     def get_updated_content(self):
#         return (
#             (timezone.make_aware(
#                 datetime.now(), timezone.get_current_timezone()
#             ) - timezone.make_aware(
#                 datetime(1970, 1, 1),
#                 timezone.get_current_timezone()
#             )).total_seconds() * 1000.0,
#             random.choice(range(0, 25)),
#         )
#
#
# def lorem_ipsum_generator():
#     for word in "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In odio ligula, consequat id libero in, efficitur suscipit dolor. Vivamus interdum justo tincidunt libero pretium congue. Sed luctus augue vitae arcu imperdiet, vitae pellentesque elit auctor. In hac habitasse platea dictumst. Nunc fermentum sem vel neque maximus viverra. Praesent tortor leo, ultricies ut bibendum in, luctus nec felis. Donec id eleifend eros. Phasellus congue sollicitudin erat sed dapibus.".split(' '):
#         yield word
#     yield '<br>'
#     yield '<br>'
#     for word in "Nullam ullamcorper dictum velit, et consequat nunc aliquam sed. Aenean ut nibh nunc. In facilisis sit amet lectus non tempor. Integer non lacinia lacus, vel venenatis dui. Sed a luctus neque. Maecenas interdum, tellus sed gravida semper, metus massa tempus quam, non tristique dui arcu nec leo. Donec iaculis ut mauris eu venenatis. Donec eu pulvinar purus, nec viverra quam. Vivamus ultricies pretium hendrerit. Fusce lobortis et mauris ut consequat. Nullam eu aliquet neque. Aenean mauris quam, cursus eget tellus sed, fringilla eleifend orci. Curabitur a pretium enim.".split(' '):
#         yield word
#     yield '<br>'
#     yield '<br>'
#     for word in "Vivamus pulvinar vehicula sem, sed cursus lorem volutpat sit amet. In id lacinia quam. Aliquam ligula velit, scelerisque in finibus id, efficitur sit amet quam. Nam sagittis semper nisl sed pharetra. Praesent ex lorem, vestibulum ac ipsum quis, finibus molestie lorem. Vivamus vehicula lacus in leo fringilla, nec fermentum nibh fermentum. Mauris tincidunt, metus et venenatis auctor, sem felis sagittis odio, a volutpat erat eros luctus enim. Nunc in velit a arcu rhoncus ultricies. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Phasellus sit amet auctor libero. Donec vitae est sodales, tincidunt magna in, ultrices arcu. Praesent blandit enim a nibh tristique placerat. Aliquam cursus euismod eros, vel ultrices massa ultrices id. Mauris eu malesuada mi. Integer ut diam semper, gravida odio ac, bibendum velit. Curabitur eget ante at eros iaculis aliquam nec commodo nisi.".split(' '):
#         yield word
#     yield '<br>'
#     yield '<br>'
#     for word in "Praesent pulvinar efficitur lorem quis feugiat. Nam pharetra iaculis lacus, ac suscipit dui. Sed aliquam feugiat purus, at interdum velit faucibus sed. Suspendisse bibendum est erat, sed pulvinar nulla laoreet sed. Aliquam nec lacus sed ante cursus consectetur at id dui. Suspendisse potenti. In posuere arcu vel erat sollicitudin, nec auctor eros vehicula. Aliquam erat volutpat. Proin ultrices blandit ex at tincidunt. Quisque porta nec est sit amet facilisis. Proin euismod nisi mattis dui dictum dictum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc vestibulum suscipit lorem, non tristique quam bibendum et. Fusce hendrerit sem a rhoncus congue.".split(' '):
#         yield word
#     yield '<br>'
#     yield '<br>'
#     for word in "Praesent maximus, massa ut porttitor egestas, enim quam tincidunt lorem, in volutpat erat metus ut quam. Nulla sodales accumsan nisl. Pellentesque sollicitudin lectus libero, et auctor diam mattis molestie. Maecenas sed venenatis dolor. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam id blandit nisl, ac fermentum arcu. Aliquam magna lorem, commodo id velit ornare, tincidunt ultricies turpis. Vivamus non velit nec erat accumsan venenatis. Phasellus molestie massa suscipit felis feugiat vestibulum. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Curabitur pellentesque mattis euismod. Donec faucibus id nulla nec imperdiet. Quisque interdum justo quis nisl feugiat, sed vehicula eros mollis. Nullam lorem justo, maximus nec viverra vitae, consequat id lectus.".split(' '):
#         yield word
#
#
# class ProgressiveLoremIpsumWidget(RealTimeWidget):
#     html_id = 'lorem_id'
#     name = 'Quick Lorem'
#     url_name = 'quick_lorem'
#     url_regex = 'realtime/quick_lorem'
#     refresh_time = 100
#     template = 'app/dashboard/display/progressive_paragraph.html'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.generator = None
#         self.reset_generator()
#
#     def reset_generator(self):
#         self.generator = lorem_ipsum_generator()
#
#     def get_content(self):
#         return ''
#
#     def get_updated_content(self):
#         try:
#             return next(self.generator)
#         except StopIteration:
#             return 'STOP'
#
#
# register_realtime(CustomRealtimeWidget)
#
#
# class CustomBox(Box):
#     lorem = register_realtime(ProgressiveLoremIpsumWidget())
#     widgets = [CustomRealtimeWidget(), lorem]
#
#     def get_widgets(self):
#         self.widgets[1].reset_generator()
#         return self.widgets
