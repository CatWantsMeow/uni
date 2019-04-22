import cx_Oracle
from django.shortcuts import redirect
from django.views.generic import TemplateView
from meow_main.db import get_connection


class UserViewMixin(TemplateView):

    def _get_user_group_name(self):
        token = self.request.COOKIES.get('token', None)
        connection = get_connection('default')
        cursor = connection.cursor()
        group_id = cursor.callfunc('authenticate', cx_Oracle.NUMBER, [token])
        print group_id
        if group_id < 0:
            group_name = None
        else:
            group_name = cursor.callfunc('get_group_name', cx_Oracle.STRING, [group_id])
        cursor.close()
        return group_name

    def get_context_data(self, **kwargs):
        context_data = super(UserViewMixin, self).get_context_data(**kwargs)
        context_data['user_group_name'] = self._get_user_group_name()
        return context_data


class HomeView(TemplateView):

    def get(self, request, **kwargs):
        return redirect('mall-list')