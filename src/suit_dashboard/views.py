# -*- coding: utf-8 -*-

"""
Inheritable views.

DashboardView for classic views and RefreshableDataView for refreshable items.
"""

from __future__ import unicode_literals

from django.views.generic import TemplateView, View

from braces.views import AjaxResponseMixin, JSONResponseMixin


class DashboardView(TemplateView):
    """
    Dashboard view.

    Overwrite class variables grid, crumbs and/or extra_context.
    Crumbs will be concatenated to all parent classes' so you don't have to
    provide the whole [Bootstrap] breadcrumbs each time.
    """

    grid = None
    crumbs = ()
    extra_context = {}

    def get_crumbs(self):
        """
        Get crumbs for navigation links.

        Returns:
            tuple: concatenated list of crumbs using these crumbs and the
                crumbs of the parent classes through __mro__.
        """
        crumbs = []
        for cls in reversed(type(self).__mro__):
            crumbs.extend(getattr(cls, 'crumbs', ()))
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
        if context.get('dashboard_grid', None) is None and self.grid:
            context['dashboard_grid'] = self.grid
        return self.render_to_response(context)


class RefreshableDataView(JSONResponseMixin, AjaxResponseMixin, View):
    """
    View for refreshable items.

    Keep track of subclasses when generating them with related decorator.

    Attributes:
        children (list): list of subclasses generated thtough decorator.
    """

    children = []

    def get_data(self):
        """
        Overwrite this function to return your refreshable data.

        Returns:
            dict: JSON-convertible data yo be used in your item/box.
        """
        return {}

    def get(self, request, *args, **kwargs):
        """
        Call to get_ajax.

        Args:
            request (): Django's request object.
            *args (): request args.
            **kwargs (): request kwargs.

        Returns:
            response: get_ajax result.
        """
        return self.get_ajax(request, *args, **kwargs)

    def get_ajax(self, request, *args, **kwargs):
        """
        Call to render_to_json_response with get_data() as data.

        Args:
            request (): Django's request object.
            *args (): request args.
            **kwargs (): request kwargs.

        Returns:
            response: render_json_response result.
        """
        return self.render_json_response(self.get_data())
