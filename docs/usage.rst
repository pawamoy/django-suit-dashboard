=====
Usage
=====

To use Django Suit Dashboard in a Django project, first add it in installed apps:

.. code:: python

	INSTALLED_APPS += [
		'suit_dashboard'
	]

And replace::

	'django.contrib.admin'

by::

	'django.contrib.admin.apps.SimpleAdminConfig'

You must of course have `django-suit`_ installed since it will only work with Suit.

.. _django-suit: http://djangosuit.com/

Quick start
-----------

Create a new application::

	./manage.py startapp dashboard

In this new application, create a sites.py module, and a custom admin site.
This custom admin site will contain your URL list:

.. code:: python

	# -*- coding: utf-8 -*-

	from __future__ import unicode_literals
	from django.contrib.admin.sites import AdminSite
	from django.conf.urls import url
	from dashboard.views import dashboard_main_view


	class DashboardSite(AdminSite):
		"""A Django AdminSite to allow registering custom dashboard views."""
		def get_urls(self):
			urls = super(DashboardSite, self).get_urls()
			custom_urls = [
					url(r'^$', self.admin_view(dashboard_main_view), name="index")
			]

			del urls[0]
			return custom_urls + urls

You can already use this admin site in your main urls.py:

.. code:: python

	from django.contrib import admin
	from dashboard.sites import DashboardSite

	admin.site = DashboardSite()
	admin.autodiscover()

But also you must create the main view, imported by the previous module:

.. code:: python

	# -*- coding: utf-8 -*-

	from __future__ import unicode_literals
	from django.shortcuts import render
	from suit_dashboard.layout import Grid, Row, Column


	def dashboard_main_view(request):
		template_name = 'dashboard/main.html'
		context = {
			'dashboard_grid': Grid([])
		}

		return render(request, template_name, context)

We will later see how to use Grid, Row and Column classes.

And finally, create the main.html template in a location where it will be found by Django:

.. code:: django+html

	{% extends "suit_dashboard/base.html" %}
	{% load i18n admin_static %}

	{% block title %}
		Title in browser tab
	{% endblock %}

	{% block dashboard_title %}
		Title on top of dashboard
	{% endblock %}

	{# Remove the breadcrumbs #}
	{% block breadcrumbs %}{% endblock %}

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

Now that you have a base, here is how you can add widgets to your admin pages.
Your widgets have to be added to a layout. You can build this layout using
Grid, Row and Column from suit_dashboard.layout. The context object sent to the
template and containing the grid must be called 'dashboard_grid'.

A Grid instance is a list of Row instances. A Row instance is a list of
Column instances (just like in Twitter Bootstrap). Each Column instance can
then contain instances of Row (again) and/or Widget.

Lets take the previous main view and add many rows and columns,
just to see the result:

.. code:: python

	from suit_dashboard.widgets import Widget

	def dashboard_main_view(request):
		template_name = 'dashboard/main.html'
		context = {
			'dashboard_grid': Grid([
				Row([
					Column([
						Widget(title='Row 1 column 1 widget 1'),
						Widget(title='Row 1 column 1 widget 2')
					], width=6),
					Column([
						Widget(title='Row 1 column 2 widget 1',
									 description=', '.join([str(_) for _ in range(5, 15)])),
						Widget(title='Row 1 column 2 widget 2')
					], width=6),
				]),
				Row([
					Column([
						Widget(title='Row 2 column 1 widget 1'),
						Widget(title='Row 2 column 1 widget 2')
					], width=3),
					Column([
						Widget(title='Row 2 column 2 widget 1'),
						Widget(title='Row 2 column 2 widget 2',
									 description=', '.join([str(_) for _ in range(5, 200)]))
					], width=5),
					Column([
						Row([
							Column([
								Widget(title='R2 C3 R1 C1 W1'),
								Widget(title='R2 C3 R1 C1 W2')
							], width=12)
						]),
						Row([
							Column([
								Widget(title='R2 C3 R2 C1 W1'),
								Widget(title='R2 C3 R2 C1 W2')
							], width=12)
						])
					], width=4),
				])
			])
		}

		return render(request, template_name, context)

Go take a look!

This is not very fancy... And this code is not clean.
Widgets can be created in a separate module.

Widgets
-------

Here is an example of Widget showing information about the machine.

.. code:: python

	# -*- coding: utf-8 -*-
	# dashboard/widgets.py

	from __future__ import unicode_literals
	import platform
	import psutil

	from suit_dashboard.widgets import Widget, WidgetGroup, WidgetItem


	class WidgetMachine(Widget):
		@property
		def title(self):
			return 'Machine'

		@property
		def description(self):
			return 'Information about the hosting machine.'

		@property
		def context(self):
			return [
				WidgetGroup(
					'sysspec', 'System specifications',
					[
							WidgetItem('hostname', 'Hostname', platform.node()),
							WidgetItem('system', 'System', '%s, %s, %s' % (
									platform.system(),
									' '.join(platform.linux_distribution()),
									platform.release())),
							WidgetItem('architecture', 'Architecture', ' '.join(platform.architecture())),
							WidgetItem('processor', 'Processor', platform.processor()),
							WidgetItem('python_version', 'Python version', platform.python_version())
					],
					display=WidgetGroup.AS_TABLE,
					classes='table-bordered table-condensed '
									'table-hover table-striped'
				)
			]

Use it in a layout:

.. code:: python

	# -*- coding: utf-8 -*-
	# dashboard/views.py

	from __future__ import unicode_literals
	from django.shortcuts import render
	from suit_dashboard.layout import Grid, Row, Column
	from dashboard.widgets import WidgetMachine


	def dashboard_main_view(request):
		template_name = 'dashboard/main.html'
		context = {
			'dashboard_grid': Grid([
				Row([
					Column([WidgetMachine()], width=6)
				]),
			])
		}

		return render(request, template_name, context)
