=========
Changelog
=========

2.0.6 (2017-05-29)
==================

- Update to support django-app-settings 0.3.0.

2.0.5 (2017-05-29)
==================

- Update tests.

2.0.4 (2017-05-29)
==================

* Fix `dashboard_js` block not being added while rendering when not using Django Suit.
* Add demo project.
* Add diagram in documentation.
* Remove display templates (if you were using them, please copy them
  back from the docs into your project).

2.0.3 (2017-04-10)
==================

* Use instance's crumbs.
* As for boxes, accept keyword arguments to set in widgets.
* Fix real-time setting default ``url_name``.
* Remove ``PartialResponse`` from ``__init__.__all__``.
* Update breadcrumbs to strictly match classic and Suit's styles.


2.0.2 (2017-04-03)
==================

* Add title option to views.
* Don't display crumbs if none.
* Move PartialResponse into real-time function to avoid ``AppsNotReady`` (fix #30).

2.0.1 (2017-03-29)
==================

* All objects are now importable directly from ``suit_dashboard``.
* Moved application settings into an ``apps`` module.


2.0.0 (2017-03-20)
==================

The version 2.0.0 adds more flexibility and simplicity of usage
to the application. It doesn't try to be smart anymore, nor force usage
of particular CSS/JS libraries.

* Add app settings (currently just SUIT_DASH_DEFAULT_TIME_INTERVAL).
* Uncouple from Django Suit. The name will remain django-suit-dashboard because
  it was originally designed to work within Django Suit. The application sees
  if Suit is in use and set the breadcrumbs accordingly (it supports both
  classic and Suit style).
* A ``suit`` variable is injected into template's context so you can update
  behavior according to it. Use it like ``{% if suit %}...{% endif %}``.
* Various API changes, check the documentation to see them.

1.0.3 (2016-12-31)
==================

* Updates from upstream cookiecutter-pydjama.

1.0.2 (2016-10-19)
==================

* Fix Python 3 compatibility.

1.0.1 (2016-09-30)
==================

* Fix type check of column elements.
* Fix missing dependency django-braces.

1.0.0 (2016-09-01)
==================

Various fixes and behavior changes.

* Fix bumpversion configuration.
* Add possibility to give grid as argument to super get.
* Change persistent to false (unpredictable behavior with cache?).
* Fix changing URL for refreshable items.
* Update docs, decorator now supports args or not, fix case when multiple series in template.
* Allow lazy initialization for boxes (or not).
* Change Box behavior, improve refreshable decorator, implement JSON refresh in box template.
* Fix URLs in README.
* Configure isort to understand django apps, fix imports order.
* Add refreshable data view and decorator and display.
* Fix inconsistent title error.
* Remove BSD2 link from README.
* Display item names only if they exist.
* Change context to kwargs, add context as argument.
* Fix issue #4.
* Fix overwriting default value if variable's parent was defined. Also log exceptions in console.
* Add id for each item in table.
* Move element title inside 'group' condition.
* Fix issue #1.

0.1.0 (2016-04-19)
==================

* Alpha release on PyPI.
