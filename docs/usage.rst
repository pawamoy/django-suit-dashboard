=====
Usage
=====

To use Django Suit Dashboard in a Django project,
first add it in installed apps:

.. code:: python

  INSTALLED_APPS += [
    'suit_dashboard'
  ]

And replace::

  'django.contrib.admin'

by::

  'django.contrib.admin.apps.SimpleAdminConfig'

You must of course have `django-suit`_ installed
since it will only work with Suit.

.. _django-suit: http://djangosuit.com/

Quick start
-----------

Create a new application::

  ./manage.py startapp dashboard

In this new application, create a `sites.py` module, and a custom admin site.
This custom admin site will contain your URL list:

.. code:: python

  # -*- coding: utf-8 -*-
  # dashboard/sites.py

  from __future__ import unicode_literals
  from django.contrib.admin.sites import AdminSite
  from django.conf.urls import url
  from dashboard.views import HomeView


  class DashboardSite(AdminSite):
    """A Django AdminSite to allow registering custom dashboard views."""
    def get_urls(self):
      urls = super(DashboardSite, self).get_urls()
      custom_urls = [
          url(r'^$', self.admin_view(HomeView.as_view()), name='index')
      ]

      del urls[0]
      return custom_urls + urls

You can use this admin site in your main `urls.py`:

.. code:: python

  from django.contrib import admin
  from dashboard.sites import DashboardSite

  admin.site = DashboardSite()
  admin.sites.site = admin.site  # >= Django 1.9.5
  admin.autodiscover()

But before, you must create the `HomeView`, imported by your custom admin site:

.. code:: python

  # -*- coding: utf-8 -*-
  # dashboard/views.py

  from __future__ import unicode_literals
  from django.shortcuts import render
  from django.utils.translation import ugettext_lazy as _
  from suit_dashboard.layout import Grid, Row, Column
  from suit_dashboard.views import DashboardView


  class HomeView(DashboardView):
      template_name = 'dashboard/main.html'
      crumbs = (
          {'url': 'admin:index', 'name': _('Home')},
      )
      grid = Grid()  # our page will be empty for now

We will later see how to use Grid, Row and Column classes.

And finally, create the `dashboard/main.html` template in a location
where it will be found by Django:

.. code:: html+django

  {% extends "suit_dashboard/base.html" %}
  {% load i18n admin_static %}

  {% block title %}
    Title in browser tab
  {% endblock %}

  {% block dashboard_css %}
    <link href="{% static 'dashboard/your_main.css' %}" rel="stylesheet" media="all">
  {% endblock %}

  {# Load local Highcharts, default from Highcharts' CDN #}
  {% block dashboard_highcharts_js %}
    <script src="{% static "path/to/your/highcharts/highcharts.js" %}"></script>
    <script src="{% static "path/to/your/highcharts/highcharts-more.js" %}"></script>
  {% endblock %}


Layout
------

Now that you have a base, here is how you can add content to your admin pages.
Your content have to be added to a layout. You can build this layout using
Grid, Row and Column from `suit_dashboard.layout`.

A Grid instance is a list of Row instances. A Row instance is a list of
Column instances (just like in Twitter Bootstrap). Each Column instance can
then contain instances of Row (again) and/or Box.

Lets take the previous view and add many rows and columns,
just to see the result:

.. code:: python

  # -*- coding: utf-8 -*-
  # dashboard/views.py

  from __future__ import unicode_literals
  from django.shortcuts import render
  from django.utils.translation import ugettext_lazy as _
  from suit_dashboard.layout import Grid, Row, Column
  from suit_dashboard.views import DashboardView
  from suit_dashboard.box import Box

  class HomeView(DashboardView):
      template_name = 'dashboard/main.html'
      crumbs = (
          {'url': 'admin:index', 'name': _('Home')},
      )
      grid = Grid(
        Row(
          Column(
            Box(title='Row 1 column 1 box 1'),
            Box(title='Row 1 column 1 box 2'),
            width=6),
          Column(
            Box(title='Row 1 column 2 box 1'),
            Box(title='Row 1 column 2 box 2'),
            width=6),
        ),
        Row(
          Column(
            Box(title='Row 2 column 1 box 1'),
            Box(title='Row 2 column 1 box 2'),
            width=3),
          Column(
            Box(title='Row 2 column 2 box 1'),
            Box(title='Row 2 column 2 box 2'),
            width=5),
          Column(
            Row(
              Column(
                Box(title='R2 C3 R1 C1 B1'),
                Box(title='R2 C3 R1 C1 B2'),
                width=12)
            ),
            Row(
              Column(
                Box(title='R2 C3 R2 C1 B1'),
                Box(title='R2 C3 R2 C1 B2'),
                width=12)
            ),
            width=4),
        )
      )


Go take a look!

This is not very fancy... And this code is not clean.
Boxes can be created in a separate module.

Boxes
-----

Lets create a box showing information about the machine.

.. code:: python

  # -*- coding: utf-8 -*-
  # dashboard/boxes.py

  from __future__ import unicode_literals
  import platform
  import psutil
  from django.utils.translation import ugettext as _
  from suit_dashboard.box import Box, Item


  class BoxMachine(Box):
      def get_title(self):
          return _('Machine')

      def get_description(self):
          return _('Information about the hosting machine for my website.')

      # The get_items function is the main function here. It will define
      # what are the contents of the box.
      def get_items(self):
          # Retrieve and format uptime (will not work on Windows)
          with open('/proc/uptime') as f:
              s = timedelta(seconds=float(f.readline().split()[0])).total_seconds()
              uptime = _('%d days, %d hours, %d minutes, %d seconds') % (
                  s // 86400, s // 3600 % 24, s // 60 % 60, s % 60)

          # Create a first item (box's content) with the machine info
          item_info = Item(
              html_id='sysspec', name=_('System specifications'),
              display=Item.AS_TABLE,
              # Since we use AS_TABLE display, value must be a list of tuples
              value=(
                  (_('Hostname'), platform.node()),
                  (_('System'), '%s, %s, %s' % (
                      platform.system(),
                      ' '.join(platform.linux_distribution()),
                      platform.release())),
                  (_('Architecture'), ' '.join(platform.architecture())),
                  (_('Processor'), platform.processor()),
                  (_('Python version'), platform.python_version()),
                  (_('Uptime'), uptime)
              ),
              classes='table-bordered table-condensed '
                      'table-hover table-striped'
          )

          # Retrieve RAM and CPU data
          ram = psutil.virtual_memory().percent
          cpu = psutil.cpu_percent()

          # Green, orange, red or grey color for usage/idle
          green, orange, red, grey = '#00FF38', '#FFB400', '#FF3B00', '#EBEBEB'

          ram_color = green  # default
          if ram >= 75:
              ram_color = red
          elif ram >= 50:
              ram_color = orange

          cpu_color = green  # default
          if cpu >= 75:
              cpu_color = red
          elif cpu >= 50:
              cpu_color = orange

          # Now create a chart to display CPU and RAM usage
          chart_options = {
              'chart': {
                  'type': 'bar',
                  'height': 200,
              },
              'title': {
                  'text': _('RAM and CPU usage')
              },
              'xAxis': {
                  'categories': [_('CPU usage'), _('RAM usage')]
              },
              'yAxis': {
                  'min': 0,
                  'max': 100,
                  'title': {
                      'text': _('Percents')
                  }
              },
              'tooltip': {
                  'percentageDecimals': 1
              },
              'legend': {
                  'enabled': False
              },
              'plotOptions': {
                  'series': {
                      'stacking': 'normal'
                  }
              },
              'series': [{
                  'name': _('CPU idle'),
                  'data': [{'y': 100 - cpu, 'color': grey}, {'y': 0}],
              }, {
                  'name': _('CPU used'),
                  'data': [{'y': cpu, 'color': cpu_color}, {'y': 0}],
              }, {
                  'name': _('RAM free'),
                  'data': [{'y': 0}, {'y': 100 - ram, 'color': grey}],
              }, {
                  'name': _('RAM used'),
                  'data': [{'y': 0}, {'y': ram, 'color': ram_color}],
              }]
          }

          # Create the chart item
          item_chart = Item(
              html_id='highchart-machine-usage',
              name=_('Machine usage'),
              value=chart_options,
              display=Item.AS_HIGHCHARTS)

          # Return the list of items
          return [item_info, item_chart]

Now we can use this box in our previous layout:

.. code:: python

  # -*- coding: utf-8 -*-
  # dashboard/views.py

  from __future__ import unicode_literals
  from django.shortcuts import render
  from django.utils.translation import ugettext_lazy as _
  from suit_dashboard.layout import Grid, Row, Column
  from suit_dashboard.views import DashboardView
  from suit_dashboard.box import Box

  class HomeView(DashboardView):
      template_name = 'dashboard/main.html'
      crumbs = (
          {'url': 'admin:index', 'name': _('Home')},
      )
      grid = Grid(Row(Column(BoxMachine(), width=6)))


Refreshable content
-------------------

Lets face it, having the CPU and RAM usage at time T is not very useful.
It would be great to have the chart updated each second! Well you can,
using the `RefreshableDataView` from `suit_dashboard.views`. But first,
we have to split our `get_items` function a bit.

We need a function that will return the chart dictionary, and only that.
And we will decorate it with `refreshable`:

.. code:: python

  # -*- coding: utf-8 -*-
  # dashboard/charts.py

  from __future__ import unicode_literals
  import psutil
  from django.utils.translation import ugettext_lazy as _
  from suit_dashboard.decorators import refreshable

  @refreshable
  def machine_usage_chart():
      # Retrieve RAM and CPU data
      ram = psutil.virtual_memory().percent
      cpu = psutil.cpu_percent()

      # ... like before (save you some scrolling)

      return chart_options

Now in the `get_items` function:

.. code:: python

  # -*- coding: utf-8 -*-
  # dashboard/boxes.py

  from __future__ import unicode_literals
  import platform
  import psutil
  from django.utils.translation import ugettext as _
  from suit_dashboard.box import Box, Item
  from dashboard.stats import machine_usage_stats


  class BoxMachine(Box):
      # ... title and description function

      def get_items(self):
          # ... create the item_info object

          item_chart = Item(
              html_id='highchart-machine-usage', name=_('Machine usage'),
              value=machine_usage_stats(),
              display=Item.AS_HIGHCHARTS)

          return [item_info, item_chart]

One last step... in your `DashboardSite` (in `sites.py`), you have to add
the automatically generated urls, used for refreshing, like this:

.. code:: python

  from suit_dashboard.urls import get_refreshable_urls

  class DashboardSite(AdminSite):
      def get_urls(self):
          # ...
          return custom_urls + urls + get_refreshable_urls(self.admin_view)

And that's it! You chart will now be refreshed each 5 seconds by default.
To change the refresh time, specify the milliseconds in the decorator:

.. code:: python

  @refreshable(refresh_time=1000)
  def machine_usage_chart():
      # ...

If later you don't want it to be "refreshable", just remove the decorator above
the function `machine_usage_chart`.

Nested views
------------

