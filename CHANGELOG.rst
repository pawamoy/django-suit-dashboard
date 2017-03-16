=========
Changelog
=========

2.0.0 (2017-03-15)
==================

The version 2.0.0 adds more flexibility and simplicity of usage
to the application. It doesn't try to be smart anymore, nor force usage
of particular CSS/JS libraries.

* Add app settings (currenly just SUIT_DASH_DEFAULT_TIME_INTERVAL).
* Uncouple from django-suit. The name will remain django-suit-dashboard because
  is was originally designed to work within django-suit. The application sees
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

* Fix bumversion config.
* Add possibility to give grid as argument to super get.
* Change persistent to false (unpredictable behavior with cache?).
* Fix changing url for refreshable items.
* Update docs, decorator now supports args or not, fix case when multiple series in template.
* Allow lazy initialization for boxes (or not).
* Change Box behaviour, improve refreshable decorator, implement JSON refresh in box template.
* Fix urls in README.
* Configure isort to understand django apps, fix imports order.
* Add refreshable data view and decorator and display.
* Fix inconsistent title error.
* Remove BSD2 link from README.
* Display item names only if they exist.
* Change context to kwargs, add context as arg.
* Fix issue #4.
* Fix overwriting default value if variable's parent was defined. Also log exceptions in console.
* Add id for each item in table.
* Move element title inside 'group' condition.
* Fix issue #1.

0.1.0 (2016-04-19)
==================

* Alpha release on PyPI.
