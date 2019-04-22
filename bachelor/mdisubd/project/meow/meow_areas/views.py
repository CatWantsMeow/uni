from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from meow_areas.db import get_shopping_malls, get_shopping_mall, get_shopping_areas, create_shopping_mall, \
    delete_shopping_mall, get_shopping_area, create_shopping_area, delete_shopping_area
from meow_areas.forms import ShoppingMallForm, ShoppingAreaForm
from meow_auth.db import get_tenant_id
from meow_contracts.db import get_tenant_rent_requests
from meow_main.db import has_privilege
from meow_main.views import UserViewMixin


class ShoppingMallCreateView(UserViewMixin, TemplateView):

    template_name = 'meow_areas/create_or_edit_page.html'

    def get(self, request, **kwargs):
        context_data = self.get_context_data(**kwargs)
        token = request.COOKIES.get('token')
        if not has_privilege(token, 'create_or_update_shopping_mall'):
            raise Http404()

        mall_id = kwargs.get('mall_id', None)
        if mall_id is not None:
            mall = get_shopping_mall(mall_id)
            if mall is None:
                raise Http404()
            data = {
                'name': mall[1],
                'description': mall[2],
                'floors_number': mall[3],
                'parking_size': mall[4],
                'location_id': mall[5][0],
            }
            context_data['form'] = ShoppingMallForm(data)
        else:
            context_data['form'] = ShoppingMallForm()

        return render(request, self.template_name, context=context_data)

    def post(self, request, **kwargs):
        form = ShoppingMallForm(request.POST)
        context = self.get_context_data(**kwargs)
        mall_id = kwargs.get('mall_id', None)
        if form.is_valid():
            created = create_shopping_mall(context['user_group_name'], mall_id, form.cleaned_data)
            if created:
                if mall_id:
                    return redirect('mall-detail', mall_id)
                else:
                    return redirect('mall-list')
            else:
                pass
                # form.add_error('non_fields_errors', 'Failed to create shopping mall :C')

        context['form'] = form
        return render(request, self.template_name, context=context)


class ShoppingMallListView(UserViewMixin, TemplateView):

    template_name = 'meow_areas/mall_list.html'

    def get_context_data(self, **kwargs):
        context = super(ShoppingMallListView, self).get_context_data(**kwargs)
        context['malls'] = get_shopping_malls()
        return context


class ShoppingMallDetailView(UserViewMixin, TemplateView):

    template_name = 'meow_areas/mall.html'
    
    def get_context_data(self, **kwargs):
        token = self.request.COOKIES.get('token')
        mall_id = kwargs.get('mall_id', None)
        context = super(ShoppingMallDetailView, self).get_context_data(**kwargs)
        mall = get_shopping_mall(mall_id)
        if mall is None:
            raise Http404('Shopping mall with specified id does not exists')
        context['areas'] = get_shopping_areas(mall_id)
        tenant_id = get_tenant_id(token)
        context['rent_request_ids'] = [rr[0] for rr in get_tenant_rent_requests(tenant_id)]
        context['mall'] = get_shopping_mall(mall_id)
        return context


class ShoppingMallDeleteView(UserViewMixin, TemplateView):

    def get(self, request, **kwargs):
        mall_id = kwargs.get('mall_id', None)
        context = self.get_context_data(**kwargs)
        result = delete_shopping_mall(context['user_group_name'], mall_id)
        if result:
            return redirect('mall-list')
        else:
            raise Http404()


class ShoppingAreaCreateView(UserViewMixin, TemplateView):

    template_name = 'meow_areas/create_or_edit_page.html'

    def get(self, request, **kwargs):
        context_data = self.get_context_data(**kwargs)
        token = request.COOKIES.get('token')
        if not has_privilege(token, 'create_or_update_shopping_area'):
            raise Http404()

        area_id = kwargs.get('area_id', None)
        if area_id is not None:
            area = get_shopping_area(area_id)
            if area is None:
                raise Http404()
            data = {
                'area': area[1],
                'description': area[2],
                'landlord_id': area[4],
                'price_id': area[5],
            }
            context_data['form'] = ShoppingAreaForm(data)
        else:
            context_data['form'] = ShoppingAreaForm()

        return render(request, self.template_name, context=context_data)

    def post(self, request, **kwargs):
        form = ShoppingAreaForm(request.POST)
        context = self.get_context_data(**kwargs)
        area_id = kwargs.get('area_id', None)
        mall_id = kwargs.get('mall_id', None)
        if form.is_valid():
            created = create_shopping_area(context['user_group_name'], area_id, mall_id, form.cleaned_data)
            if created:
                return redirect('mall-detail', mall_id)
            else:
                pass
                # form.add_error('non_fields_errors', 'Failed to create shopping mall :C')

        context['form'] = form
        return render(request, self.template_name, context=context)


class ShoppingAreaDeleteView(UserViewMixin, TemplateView):

    def get(self, request, **kwargs):
        mall_id = kwargs.get('mall_id', None)
        area_id = kwargs.get('area_id', None)
        context = self.get_context_data(**kwargs)
        result = delete_shopping_area(context['user_group_name'], area_id)
        if result:
            return redirect('mall-detail', mall_id)
        else:
            raise Http404()