# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import random
import string

from django.views.generic import TemplateView, View

from braces.views import AjaxResponseMixin, JSONResponseMixin


class DashboardView(TemplateView):
    grid = None
    crumbs = ()
    extra_context = {}

    def get_crumbs(self):
        crumbs = []
        for cls in reversed(type(self).__mro__):
            crumbs.extend(getattr(cls, 'crumbs', ()))
        return tuple(crumbs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update(self.extra_context)
        context.update({
            'dashboard_grid': self.grid,
            'crumbs': self.get_crumbs()
        })
        return self.render_to_response(context)


class RefreshableDataView(JSONResponseMixin, AjaxResponseMixin, View):
    instances = []

    def __init__(self, func=lambda: None, name=None, regex=None):
        super(RefreshableDataView, self).__init__()
        if regex is None:
            regex = ''.join(random.SystemRandom().choice(
                string.ascii_lowercase + string.digits) for _ in range(32))
        if name is not None:
            if name in [i.name for i in RefreshableDataView.instances]:
                raise ValueError('Name "%s" is already used by another '
                                 'instance of RefreshableDataView' % name)
            RefreshableDataView.instances.append(self)

        self.regex = regex
        self.func = func
        self.name = name

    def get_data(self):
        return self.func()

    def get(self, request, *args, **kwargs):
        return self.get_ajax(request, *args, **kwargs)

    def get_ajax(self, request, *args, **kwargs):
        return self.render_json_response(self.get_data())
