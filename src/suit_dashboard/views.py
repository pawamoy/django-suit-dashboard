# -*- coding: utf-8 -*-

"""
Inheritable views.

DashboardView for classic views and RefreshableDataView for refreshable items.
"""

from __future__ import unicode_literals

from django.conf import settings
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    """
    Dashboard view.

    Overwrite class variables grid, crumbs and/or extra_context.
    Crumbs will be concatenated to all parent classes' so you don't have to
    provide the whole [Bootstrap] breadcrumbs each time.
    """

    title = 'Suit Dashboard'
    template_name = 'suit_dashboard/base.html'
    grid = None
    crumbs = ()
    extra_context = {}

    def get_crumbs(self):
        """
        Get crumbs for navigation links.

        Returns:
            tuple:
                concatenated list of crumbs using these crumbs and the
                crumbs of the parent classes through ``__mro__``.
        """
        crumbs = []
        for cls in reversed(type(self).__mro__[1:]):
            crumbs.extend(getattr(cls, 'crumbs', ()))
        crumbs.extend(list(self.crumbs))
        return tuple(crumbs)

    def get(self, request, *args, **kwargs):
        """
        Django view get function.

        Add items of extra_context, crumbs and grid to context.

        Args:
            request (): Django's request object.
            *args (): request args.
            **kwargs (): request kwargs.

        Returns:
            response: render to response with context.
        """
        context = self.get_context_data(**kwargs)
        context.update(self.extra_context)
        context['crumbs'] = self.get_crumbs()
        context['title'] = self.title
        context['suit'] = 'suit' in settings.INSTALLED_APPS
        if context.get('dashboard_grid', None) is None and self.grid:
            context['dashboard_grid'] = self.grid
        return self.render_to_response(context)
