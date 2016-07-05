# -*- coding: utf-8 -*-

from __future__ import unicode_literals

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
        context['crumbs'] = self.get_crumbs()
        if context.get('dashboard_grid', None) is None and self.grid:
            context['dashboard_grid'] = self.grid
        return self.render_to_response(context)


class RefreshableDataView(JSONResponseMixin, AjaxResponseMixin, View):
    children = []

    def get_data(self):
        return {}

    def get(self, request, *args, **kwargs):
        return self.get_ajax(request, *args, **kwargs)

    def get_ajax(self, request, *args, **kwargs):
        return self.render_json_response(self.get_data())
