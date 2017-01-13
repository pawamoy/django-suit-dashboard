
class Display(object):
    """
    Display class.

    Provide a template path and optionally javascript files paths.
    The template will be used to render a widget in HTML, and the javascript
    files will be included after the template code. These javascript files
    should contain functions to redraw completely or partially update the
    rendered HTML.
    """

    template = None
    javascript = []

    def __init__(self, template=template, javascript=javascript):
        if template != self.__class__.template:
            self.template = template
        if javascript != self.__class__.javascript:
            self.javascript = javascript

    def get_template(self):
        return self.template

    def get_javascript(self):
        return self.javascript


class ParagraphDisplay(Display):
    template = 'suit_dashboard/display/paragraph.html'


class ListDisplay(Display):
    template = 'suit_dashboard/display/list.html'


class TableDisplay(Display):
    template = 'suit_dashboard/display/paragraph.html'


class HighchartsStaticDisplay(Display):
    template = 'suit_dashboard/display/highcharts_static.html'


class HighchartsRealtimeSeries(Display):
    template = 'suit_dashboard/display/highcharts_realtime_initdynamic_update_series'

