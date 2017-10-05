=====================
Django Suit Dashboard
=====================

.. start-badges


|travis|
|codacygrade|
|codacycoverage|
|version|
|wheel|
|pyup|
|gitter|


.. |travis| image:: https://travis-ci.org/Pawamoy/django-suit-dashboard.svg?branch=master
    :target: https://travis-ci.org/Pawamoy/django-suit-dashboard/
    :alt: Travis-CI Build Status

.. |codacygrade| image:: https://api.codacy.com/project/badge/Grade/f17fe5fdb2a248efa3e9eccd4b7045a7
    :target: https://www.codacy.com/app/Pawamoy/django-suit-dashboard/dashboard
    :alt: Codacy Code Quality Status

.. |codacycoverage| image:: https://api.codacy.com/project/badge/Coverage/f17fe5fdb2a248efa3e9eccd4b7045a7
    :target: https://www.codacy.com/app/Pawamoy/django-suit-dashboard/dashboard
    :alt: Codacy Code Coverage

.. |pyup| image:: https://pyup.io/repos/github/Pawamoy/django-suit-dashboard/shield.svg
    :target: https://pyup.io/repos/github/Pawamoy/django-suit-dashboard/
    :alt: Updates

.. |version| image:: https://img.shields.io/pypi/v/django-suit-dashboard.svg?style=flat
    :target: https://pypi.org/project/django-suit-dashboard/
    :alt: PyPI Package latest release

.. |wheel| image:: https://img.shields.io/pypi/wheel/django-suit-dashboard.svg?style=flat
    :target: https://pypi.org/project/django-suit-dashboard/
    :alt: PyPI Wheel

.. |gitter| image:: https://badges.gitter.im/Pawamoy/django-suit-dashboard.svg
    :target: https://gitter.im/Pawamoy/django-suit-dashboard
    :alt: Join the chat at https://gitter.im/Pawamoy/django-suit-dashboard


.. end-badges

Create a dashboard within Django admin interface.

This application was originally designed to work within `Django Suit`_
(hence the name), but it is now decoupled from it, you can use it without Suit.

Here is a quick explanation of how it works:

- you write a base template to add CSS/JavaScript libraries (optional)
- you write a custom AdminSite to override default URLs and/or add others
- you write the corresponding views, inheriting from DashboardView
- each view render the base template (or an extended one) with a grid in
  the context (layout of rows and columns)
- columns can contain boxes of content (visual separation on the page)
- boxes can contain widgets, for which you write the HTML/CSS/JS

So basically django-suit-dashboard does not do much, it just provides a way
to create a dashboard in admin interface without touching too much to HTML
(which not everyone will approve).

.. _`Django Suit`: https://github.com/darklow/django-suit

Screenshot
==========

.. image:: https://cloud.githubusercontent.com/assets/3999221/14685134/8cde04be-0733-11e6-8eda-b59f2e2fa6c3.png
    :alt: Screenshot

License
=======

Software licensed under `ISC`_ license.

.. _ISC: https://www.isc.org/downloads/software-support-policy/isc-license/

Installation
============

::

    pip install django-suit-dashboard

Documentation
=============

`On ReadTheDocs`_

.. _`On ReadTheDocs`: http://django-suit-dashboard.readthedocs.io/

Demo project
============

Follow these instructions to run the demo locally:

.. code:: bash

  git clone https://github.com/Pawamoy/suit-dashboard-demo
  cd suit-dashboard-demo
  ./install.sh
  ^C (Ctrl-c)
  ./run.sh [with-suit]  # any non-empty arg will do

Connect to the admin interface with your system username and password `admin_password`.

Don't hesitate to send me Pull Requests to share your boxes and widgets,
I will add them into the demo pages!

Applications using Suit-Dashboard
=================================

Here is a list of Django Apps using Suit-Dashboard. You might find some
interesting ways of using it.

- `django-cerberus-ac`_: role-based access control for Django (early development)
- `django-meerkat`_: security audit application for Django sites (work in progress)

.. _`django-cerberus-ac`: https://github.com/Deavelleye/dj-CerberusAC
.. _`django-meerkat`: https://github.com/Pawamoy/django-meerkat

Development
===========

To run all the tests: ``tox``
