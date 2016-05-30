# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.views.generic import TemplateView


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
