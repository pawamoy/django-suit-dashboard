=====
Usage
=====

First you have to do a bit of setup. Then you will be able to write views
containing grids of content. A grid is composed of nested rows and columns,
and a column can contain boxes. Then, each box contains zero or more widgets.

- Setup_
- Views_
- Layout_
- Widgets_
- `Suit menu`_
- Examples_
- `API reference`_

Setup
=====

To add custom views in your admin interface, you will need 4 things:

- an ``AdminSite`` instance
- loading it in your main URLs module
- change ``django.contrib.admin`` to
  ``django.contrib.admin.apps.SimpleAdminConfig`` in ``INSTALLED_APPS``
- the views (class-based ones)

Here is an example of AdminSite:

.. code:: python

    from django.contrib.admin.sites import AdminSite
    from django.conf.urls import url

    from .views import HomeView


    class DashboardSite(AdminSite):
        def get_urls(self):
            urls = super(DashboardSite , self).get_urls()
            custom_urls = [
                url(r'^$', self.admin_view(HomeView.as_view()), name='index'),
            ]

            del urls[0]
            return custom_urls + urls

As you can see, the first URL (leading to the main page of the interface)
has been replaced by a link to our custom home view. It will allow us to add
more links to more content.

.. note::

    If you want to keep the original main page, just comment ``del urls[0]``
    and change the regular expression of the custom home URL (something like
    ``r'^dashboard/'``).
    Note that in that case, you will have to add a link to the dashboard
    somehow in the basic main page, or you will need to enter the URL manually
    in your browser.

Here the only added view is imported from a ``views`` module. We will see later
how it is written.

Before loading your admin site, change ``django.contrib.admin`` to
``django.contrib.admin.apps.SimpleAdminConfig`` in ``INSTALLED_APPS``.
Since Django Suit Dashboard works well with Django Suit, you can write
something like the following to test with and without Suit rapidly.

.. code:: python

    SUIT = True
    # SUIT = False

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'proyekt',
        'suit_dashboard'
    ]

    if SUIT:  # add suit and replace admin with SimpleAdminConfig
        INSTALLED_APPS = [
            'suit',
            'django.contrib.admin.apps.SimpleAdminConfig'
        ] + INSTALLED_APPS[1:]

Just switch on and off ``SUIT`` Boolean to test it out.

Once your admin site is set up and your installed apps OK,
load your admin site in your main URLs module:

.. code:: python

    from django.contrib import admin

    from .site import DashboardSite

    admin.site = DashboardSite()
    admin.sites.site = admin.site
    admin.autodiscover()


Views
=====

Django Suit Dashboard provides a view called ``DashboardView``, importable
from ``suit_dashboard.views``. You can inherit of this base view to create
your own views.

.. code:: python

    from suit_dashboard.views import DashboardView


    class HomeView(DashboardView):
        pass

This view will render the base template from Django Suit Dashboard. If you
want to add CSS or JS libraries in your HTML, you can specify the
``template_name`` class attribute in your view:

.. code:: python

    class HomeView(DashboardView):
        template_name = 'a/project/template.html'

In the template, you can override or overload the ``dashboard_css`` and
``dashboard_js`` blocks. Example:

.. code:: htmldjango

    {% extends "suit_dashboard/base.html" %}
    {% load static %}

    {% block dashboard_css %}
      {% if not suit %}
        <link href="{% static 'bower_components/bootstrap/dist/css/bootstrap.min.css' %}" rel="stylesheet">
        <link href="{% static 'bower_components/bootstrap/dist/css/bootstrap-theme.min.css' %}" rel="stylesheet">
      {% endif %}
    {% endblock %}

    {% block dashboard_js %}
      {% if not suit %}
        <script src="{% static 'bower_components/jquery/dist/jquery.min.js' %}"></script>
        <script src="{% static 'bower_components/bootstrap/dist/js/bootstrap.min.js' %}"></script>
      {% endif %}
      <script src="{% static 'bower_components/highcharts/highcharts.js' %}"></script>
      <script src="{% static 'bower_components/highcharts/modules/heatmap.js' %}"></script>
      <script src="{% static 'bower_components/highcharts/highcharts-more.js' %}"></script>
    {% endblock %}

.. note::

    As you can see, a ``suit`` variable is available in the context of every
    view based on ``DashboardView``. You can use it to adapt your content for
    Django Suit and classic Django styles. In the example above, we use it
    to avoid adding Bootstrap a second time, possibly colliding with
    Django Suit's own version of Bootstrap.



Nested views and breadcrumbs
----------------------------

Nesting views is useful if you want to build a page tree in your admin
interface. It is also useful to build navigation breadcrumbs.

Let's play with an example:

.. code:: python

    # in your AdminSite class

    def get_urls(self):
        urls = super(DashboardSite , self).get_urls()
        custom_urls = [
            url(r'^$', self.admin_view(HomeView.as_view()), name='index'),
            url(r'nest1/^$', self.admin_view(NestView1.as_view()), name='nest1'),
            url(r'nest1/nest2/^$', self.admin_view(NestView2.as_view()), name='nest2'),
        ]

    # in your views

    class HomeView(DashboardView):
        template_name = 'a/project/template.html'
        crumbs = ({'url': 'admin:index', 'name': _('Home')}, )


    class NestView1(HomeView):
        crumbs = ({'url': 'admin:nest1', 'name': _('Nest 1')}, )


    class NestView2(NestView1):
        crumbs = ({'url': 'admin:nest2', 'name': _('Nest 2')}, )


This set of views will automatically render a navigation bar like in the
following images (classic-styled and suit-styled):

.. image:: https://cloud.githubusercontent.com/assets/3999221/23994494/7086961c-0a45-11e7-938d-0e173eb1894e.png
    :alt: Classic-style breadcrumbs
.. image:: https://cloud.githubusercontent.com/assets/3999221/23994496/727de074-0a45-11e7-8d21-b90127bc5a6b.png
    :alt: Suit-style breadcrumbs

Each crumb is concatenated to the ones defined in parent views. You can define
several crumbs in one view:

.. code:: python

    class OtherView(DashboardView):
        crumbs = (
            {'url': 'admin:index', 'name': _('Home')},
            {'url': 'admin:nest1', 'name': _('Nest 1')},
            {'url': 'admin:nest2', 'name': _('Nest 2')},
        )

The above code will render the same navigation bar without having used
views inheritance.

Layout
======

Grid, Row, Column
-----------------

Layout is based on the concept of grids. A grid is composed of rows, each
row being composed of columns. This allows us to arrange the content on our
pages. Columns can also contain rows, so it is possible to arrange content
more precisely. Import the ``Grid``, ``Row`` and ``Column`` classes from
``suit_dashboard.layout``, and add a ``grid`` variable to your view:

.. code:: python

    from suit_dashboard.layout import Grid, Row, Column

    class HomeView(DashboardView)
        grid = Grid(
            Row(Column()),  # default width=12 (maximum)
            Row(Column(width=6), Column(width=1), Column(width=4)),
            Row(Column(  # nested rows and columns
                    Row(Column(width=10), Column(width=2)),
                    Row(Column(width=4), Column(width=6))
                width=5),
                Column(width=6)
            )
        )

Use the ``width`` keyword argument to define the width of a column. You can
use every integer from 1 to 12.

.. warning::

    If the sum of the columns' width **in one row** is superior to 12, the
    last(s) column(s) will be pushed below the first ones.

It is not mandatory that the sum of the columns' width in one row is equal to
12: for example you can have only one column in a row, with width=4. In nested
rows, the width of the columns will be relative to the parent column's width.

Boxes
-----

Adding actual content to the columns is done through the ``Box`` and ``Widget``
classes. A Box contains zero or many widgets and has optional title,
description, HTML ID, template, and context attributes.

There are two ways to define these attributes in a box:

- first is to instantiate a box with arguments,
- second is to subclass ``Box`` and use class variables.

Examples:

.. code:: python

    from suit_dashboard.layout import Box

    my_box = Box(html_id='my_box',
                 title='My box',
                 description="This is my box, don't touch it.",
                 context=any_python_object)

    class MyBox(Box):
        html_id = 'my_box'
        title = 'My box'
        description = "This is my box, don't touch it."
        context = any_python_object

    my_box = MyBox()

If you are using a subclass of ``Box``, you can still use custom parameters at
instantiation:

.. code:: python

    class MyBox(Box):
        title = 'My box'
        template = 'path/to/a/template.html'

    your_box = MyBox(title='Your box', template='path/to/another/template.html)

Most of the time, title, description, HTML ID and template will be static,
but if you need to define them in a dynamic way (computed when the template is
rendered), you can do it with properties:

.. code:: python

    class MyBox(Box):
        title = 'My box'

        @property
        def template(self):
            if something:
                return 'that/template.html'
            else:
                return 'rather/this/one.html'

.. warning::

    When using properties, you won't be able to pass custom parameters at
    box instantiation, because Python does not allow overriding properties
    of the same name with ``self.attr = attr``. To handle this, Django Suit
    Dashboard will instead store the passed value in a private attribute with
    the same name prefixed with an underscore (``self._attr = attr``).
    You can then write your property like this:

    .. code:: python

        @property
        def template(self):
            if hasattr(self, '_template'):
                return self._template

            if something:
                return 'that/template.html'
            else:
                return 'rather/this/one.html'

    This way you will be able to instantiate the box normally or with custom
    parameters.

.. note::

    The ``context`` attribute is basically not used by Django Suit Dashboard
    itself. It is only useful when you specify a custom template and want to
    pass some values to it. You will be able to use it in your template with
    ``{{ box.context }}``. For this reason, you can define a ``get_context``
    method or whatever method to return dynamic context and use it in your
    template like: ``{{ box.get_context }}``.

You can also pass extra values to a box at instantiation by passing keyword
arguments: ``box = Box(some_arg='value'`` and access them in custom template:
``{{ box.some_arg }}``.

If you declare a custom template, but also define widgets, you can include
them in your custom templates with a simple ``include`` command:

.. code:: htmldjango

    {% for widget in box.widgets %}
      {% include widget.template %}
    {% endfor %}

Widgets
=======

Widgets are composed of an HTML ID, a name, content (a Python object),
a template path and CSS classes. As for ``Box``, you have two ways to define
the values of these attributes in a ``Widget`` instance:

- with parameters at instantiation,
- with class-attributes and subclassing ``Widget``.

Example:

.. code:: python

    from suit_dashboard.widgets import Widget

    my_widget = Widget(html_id='my_widget',
                       name='My widget',
                       content='Yes this is my widget too.',
                       template='render/my/widget.html',
                       classes='awesome pretty beautiful magic')

    class MyWidget(Widget):
        html_id = 'my_widget'
        name = 'My widget'
        content = 'Yes this is my widget too.'
        template = 'render/my/widget.html'
        classes = 'awesome pretty beautiful magic'

    my_widget = MyWidget()

The usage of widgets is the same as for boxes, check the ``Boxes`` section
for more details (custom parameters at instantiation, dynamic attributes
through properties, etc.).

The content, template and HTML ID attributes are required in a widget.
The content is the data and the template is how it is rendered (you can check
the *Examples* section to see templates to render paragraphs,
lists or tables in HTML, as well as example code for Highcharts charts with
real-time updates). Name and classes attributes are optional.

Real-time widgets
-----------------

What we call a real-time widget here is a widget that is constantly updated
with Ajax calls returning JSON contents. Django Suit Dashboard can
*automatically* generate the view that will return JSON contents. What you
have to do is to:

- add the generated URLs to your AdminSite URLs: import ``get_realtime_urls``
  from ``suit_dashboard.urls`` and use it like this in the ``get_urls`` method
  of your AdminSite:

  .. code:: python

      return custom_urls + get_realtime_urls(self.admin_view) + urls

- subclass the ``Widget`` class,
- add a ``get_updated_content`` method. This method should return any Python
  object that can be serialized in JSON format,
- (optionally) add ``url_name``, ``url_regex`` and ``time_interval`` attributes
  as class attributes.

Then when instantiating your widget, pass it through the
``realtime`` method, importable from ``suit_dashboard.widgets``. Example:

.. code:: python

    from datetime import datetime

    from suit_dashboard.layout import Box
    from suit_dashboard.widgets import Widget, realtime

    class RealtimeWidget(Widget):
        html_id = 'realtime_widget'
        template = 'some/template.html'
        content = None  # initial content

        url_name = 'realtime_widget'
        url_regex = 'realtime/realtime_widget'
        time_interval = 500  # in milliseconds

        def get_updated_content():
            return datetime.now()

    class MyBox(Box):
        widgets = [realtime(RealtimeWidget())]

You can also specify the ``url_name``, ``url_regex`` and ``time_interval``
attributes as parameters of ``realtime``:

.. code:: python

    class MyBox(Box):
        widgets = [realtime(RealtimeWidget(),
                            url_name='realtime_widget'
                            url_regex='realtime/realtime_widget'
                            time_interval=500)]

.. important::

    The call to ``realtime`` **must** be run when **starting the server**,
    not at execution time. If not ran at start-up, the widget will not be
    registered when ``get_realtime_urls`` is called in ``AdminSite.get_urls``,
    and therefore the URL will not be loaded, resulting in the URL not being
    found by Django.

The default time interval is set to 1000 (1 second). You can change it with
the ``SUIT_DASH_DEFAULT_TIME_INTERVAL`` parameter in your project settings.

You still have to write the widget's template with the JSON call, but here
is good starting point:

.. code:: htmldjango

    <div id="{{ widget.html_id }}" class="box-widget {{ widget.classes }}">
      <!-- initial content here -->
    </div>
    {% with widget_url='admin:'|add:widget.url_name %}
      <script>
        setInterval(function() {
          $.getJSON("{% url widget_url %}", function(updated_content) {
            <!-- do something with updated_content -->
          });
        }, {{ widget.time_interval }});
      </script>
    {% endwith %}

.. note::

    Remember that you will need JQuery to be loaded to be able to call
    ``$.getJSON``. You can use whatever JavaScript library though, since
    you are writing the template.

Suit menu
=========

If you are using Suit in your project, it could be interesting to add
some URLs in the left sidebar. Here is configuration example:

.. code:: python

    SUIT_CONFIG = {
        'ADMIN_NAME': 'My Project Admin',
        'MENU': ('sites', {
            'label': 'Nest 1',
            'icon': 'icon-fire',
            'url': 'admin:nest1'
        }, {
            'label': 'Nest 2',
            'icon': 'icon-wrench',
            'url': 'admin:nest2',
        }, '-', {
            'label': 'Other nests',
            'icon': 'icon-road',

            # you can use the 2-layers links thanks to 'models':

            'models': (
                {
                    'label': 'Nest 2.A',
                    'url': 'admin:nest2a'
                },
                {
                    'label': 'Nest 2.B',
                    'url': 'admin:nest2b'
                }
            )
        })
    }

Which results in:

.. image:: https://cloud.githubusercontent.com/assets/3999221/24053331/022d8c94-0b39-11e7-84c4-6a18ab113c5b.png
    :alt: Django Suit Left Sidebar

Examples
========

Columns and simple widget render
--------------------------------

Full example of a view, with direct instantiation of boxes and widgets:

.. code:: python

    class DemoView(DashboardView):
        grid = Grid(Row(
            Column(
                Box(title='Demo paragraph', widgets=[Widget(
                    html_id='paragraph_widget',
                    content='This is an example of paragraph render.',
                    template='paragraph.html')]),
                Box(title='Demo list', widgets=[Widget(
                    html_id='list_widget',
                    content=['This is', 'an example of', 'list render.'],
                    template='list.html')]), width=6),
            Column(
                Box(title='Demo table', widgets=[Widget(
                    html_id='table_widget',
                    content=[
                        ['This', 'is', 'an example'],
                        ['of', 'table', 'render']],
                    template='table.html')]), width=6)))

.. code:: htmldjango

    {# paragraph.html #}

    <div id="{{ widget.html_id }}" class="box-widget widget-paragraph">
      <p class="{{ widget.classes }}">
        {% if widget.name %}
          <span class="box-widget-name">{{ widget.name }}</span>
        {% endif %} <span class="box-widget-content">
          {{ widget.content|linebreaksbr }}
        </span>
      </p>
    </div>

.. code:: htmldjango

    {# list.html #}

    <div id="{{ widget.html_id }}"  class="box-widget widget-list">
      {% if widget.name %}<h2 class="box-widget-name">{{ widget.name }}</h2>{% endif %}
      <ul class="list {{ widget.classes }}">
        {% for li in widget.content %}
          <li class="box-widget-content">{{ li|linebreaksbr }}</li>
        {% endfor %}
      </ul>
    </div>

.. code:: htmldjango

    {# table.html #}

    <div id="{{ widget.html_id }}" class="box-widget widget-table">
      {% if widget.name %}<h2 class="box-widget-name">{{ widget.name }}</h2>{% endif %}
      <table class="table {{ widget.classes }}">
        <tbody>
          {% for line in widget.content %}
            <tr>
              {% for value in line %}
                <td class="box-widget-content">{{ value|linebreaksbr }}</td>
              {% endfor %}
            </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>

Rendering (classic):

.. image:: https://cloud.githubusercontent.com/assets/3999221/24045289/d4aba428-0b1e-11e7-9133-23748ade582c.png
    :alt: Classic Demo View

Rendering (Suit):

.. image:: https://cloud.githubusercontent.com/assets/3999221/24045285/d21ba2bc-0b1e-11e7-96df-e9e868914403.png
    :alt: Suit Demo View

Real-time Highcharts widget
---------------------------

Real-time widget that draws a curve with random points between 0 and 25.
A point is added every second, a maximum of 30 points is shown, then the
interval shifts on the right.

The widget:

.. code:: python

    import json
    import random


    class RandomCurveWidget(Widget):
        html_id = 'random_curve_widget'
        name = 'Random Curve Widget'
        template = 'random_curve.html'
        url_name = 'random_curve'
        url_regex = 'realtime/random_curve'
        max_points = 30
        time_interval = 1000

        # initial content
        content = json.dumps({
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
        })

        # get random points
        def get_updated_content(self):
            return (
                (timezone.make_aware(
                    datetime.now(), timezone.get_current_timezone()
                ) - timezone.make_aware(
                    datetime(1970, 1, 1),
                    timezone.get_current_timezone()
                )).total_seconds() * 1000.0,
                random.choice(range(0, 25)),
            )

The template:

.. code:: htmldjango

    {% load static %}
    <script src="{% static 'bower_components/jquery/dist/jquery.min.js' %}"></script>
    <script src="{% static 'bower_components/highcharts/highcharts.js' %}"></script>
    <div class="box-widget {{ widget.classes }}">
      {% if widget.name %}<h2 class="box-widget-name">{{ widget.name }}</h2>{% endif %}
      <div class="box-widget-content" id="{{ widget.html_id }}"></div>
      {% with chart_url='admin:'|add:widget.url_name %}
        <script>
          var dataset = {{ widget.content|safe }};
          var chart = $('#{{ widget.html_id }}').highcharts(dataset);

          $(function () {
            setInterval(function() {
              $.getJSON("{% url chart_url %}", function(refreshed_data) {
                var chart = $('#{{ widget.html_id }}').highcharts();
                var shift = false;
                if (chart.series[0].points.length >= {{ widget.max_points }}) {
                  shift = true;
                }
                chart.series[0].addPoint(refreshed_data, false, shift);
                chart.redraw();
              });
            }, {{ widget.time_interval }});
          });
        </script>
      {% endwith %}
    </div>

The view:

.. code:: python

    from suit_dashboard.views import DashboardView
    from suit_dashboard.layout import Grid, Row, Column, Box
    from suit_dashboard.widgets import realtime

    from .widgets import RandomCurveWidget


    class RandomCurveView(DashboardView):
        grid = Grid(Row(Column(Box(widgets=[realtime(RandomCurveWidget())]))))

Rendering:

.. image:: https://cloud.githubusercontent.com/assets/3999221/24049014/fee58b9e-0b2a-11e7-804f-ce8ab85258ee.gif
    :alt: Random Curve Real-Time

Progressive Lorem Ipsum
-----------------------

.. code:: python

    def lorem_ipsum_generator():
        for word in "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In odio ligula, consequat id libero in, efficitur suscipit dolor. Vivamus interdum justo tincidunt libero pretium congue. Sed luctus augue vitae arcu imperdiet, vitae pellentesque elit auctor. In hac habitasse platea dictumst. Nunc fermentum sem vel neque maximus viverra. Praesent tortor leo, ultricies ut bibendum in, luctus nec felis. Donec id eleifend eros. Phasellus congue sollicitudin erat sed dapibus.".split(' '):
            yield word
        yield '<br>'
        yield '<br>'
        for word in "Nullam ullamcorper dictum velit, et consequat nunc aliquam sed. Aenean ut nibh nunc. In facilisis sit amet lectus non tempor. Integer non lacinia lacus, vel venenatis dui. Sed a luctus neque. Maecenas interdum, tellus sed gravida semper, metus massa tempus quam, non tristique dui arcu nec leo. Donec iaculis ut mauris eu venenatis. Donec eu pulvinar purus, nec viverra quam. Vivamus ultricies pretium hendrerit. Fusce lobortis et mauris ut consequat. Nullam eu aliquet neque. Aenean mauris quam, cursus eget tellus sed, fringilla eleifend orci. Curabitur a pretium enim.".split(' '):
            yield word
        yield '<br>'
        yield '<br>'
        for word in "Vivamus pulvinar vehicula sem, sed cursus lorem volutpat sit amet. In id lacinia quam. Aliquam ligula velit, scelerisque in finibus id, efficitur sit amet quam. Nam sagittis semper nisl sed pharetra. Praesent ex lorem, vestibulum ac ipsum quis, finibus molestie lorem. Vivamus vehicula lacus in leo fringilla, nec fermentum nibh fermentum. Mauris tincidunt, metus et venenatis auctor, sem felis sagittis odio, a volutpat erat eros luctus enim. Nunc in velit a arcu rhoncus ultricies. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Phasellus sit amet auctor libero. Donec vitae est sodales, tincidunt magna in, ultrices arcu. Praesent blandit enim a nibh tristique placerat. Aliquam cursus euismod eros, vel ultrices massa ultrices id. Mauris eu malesuada mi. Integer ut diam semper, gravida odio ac, bibendum velit. Curabitur eget ante at eros iaculis aliquam nec commodo nisi.".split(' '):
            yield word
        yield '<br>'
        yield '<br>'
        for word in "Praesent pulvinar efficitur lorem quis feugiat. Nam pharetra iaculis lacus, ac suscipit dui. Sed aliquam feugiat purus, at interdum velit faucibus sed. Suspendisse bibendum est erat, sed pulvinar nulla laoreet sed. Aliquam nec lacus sed ante cursus consectetur at id dui. Suspendisse potenti. In posuere arcu vel erat sollicitudin, nec auctor eros vehicula. Aliquam erat volutpat. Proin ultrices blandit ex at tincidunt. Quisque porta nec est sit amet facilisis. Proin euismod nisi mattis dui dictum dictum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc vestibulum suscipit lorem, non tristique quam bibendum et. Fusce hendrerit sem a rhoncus congue.".split(' '):
            yield word
        yield '<br>'
        yield '<br>'
        for word in "Praesent maximus, massa ut porttitor egestas, enim quam tincidunt lorem, in volutpat erat metus ut quam. Nulla sodales accumsan nisl. Pellentesque sollicitudin lectus libero, et auctor diam mattis molestie. Maecenas sed venenatis dolor. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam id blandit nisl, ac fermentum arcu. Aliquam magna lorem, commodo id velit ornare, tincidunt ultricies turpis. Vivamus non velit nec erat accumsan venenatis. Phasellus molestie massa suscipit felis feugiat vestibulum. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Curabitur pellentesque mattis euismod. Donec faucibus id nulla nec imperdiet. Quisque interdum justo quis nisl feugiat, sed vehicula eros mollis. Nullam lorem justo, maximus nec viverra vitae, consequat id lectus.".split(' '):
            yield word


    class ProgressiveLoremIpsumWidget(Widget):
        html_id = 'lorem_id'
        name = 'Quick Lorem'
        url_name = 'quick_lorem'
        url_regex = 'realtime/quick_lorem'
        time_interval = 100
        template = 'progressive_paragraph.html'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.generator = None
            self.reset_generator()

        def reset_generator(self):
            self.generator = lorem_ipsum_generator()

        def get_content(self):
            return ''

        def get_updated_content(self):
            try:
                return next(self.generator)
            except StopIteration:
                return 'STOP'


    class HomeBox(Box):
        widgets = [
            realtime(ProgressiveLoremIpsumWidget())
        ]

        def get_widgets(self):
            self.widgets[0].reset_generator()
            return self.widgets


.. code:: htmldjango

    <p id="{{ widget.html_id }}" class="box-widget {{ widget.classes }}"></p>
    {% with widget_url='admin:'|add:widget.url_name %}
      <script>
        var interval = setInterval(function() {
          $.getJSON("{% url widget_url %}", function(next_word) {
            if (next_word === 'STOP') {
              clearInterval(interval);
            }
            else {
              $('#{{ widget.html_id }}').append(' ' + next_word);
            }
          });
        }, {{ widget.time_interval }});
      </script>
    {% endwith %}

API reference
=============

``suit_dashboard``
------------------

.. automodule:: suit_dashboard
    :members:

``suit_dashboard.layout``
-------------------------

.. automodule:: suit_dashboard.layout
    :members:

``suit_dashboard.urls``
-----------------------

.. automodule:: suit_dashboard.urls
    :members:

``suit_dashboard.views``
------------------------

.. automodule:: suit_dashboard.views
    :members:

``suit_dashboard.widgets``
--------------------------

.. automodule:: suit_dashboard.widgets
    :members:
