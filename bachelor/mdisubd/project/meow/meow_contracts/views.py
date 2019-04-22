from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from meow_auth.db import get_tenant_id, get_landlord_id
from meow_contracts.db import create_rent_request, get_tenant_rent_requests, get_tenant_rent_contracts, \
    get_landlord_rent_requests, get_landlord_rent_contracts, delete_rent_contract, start_rent, end_rent, \
    get_rent_contract, create_rent_contract, delete_rent_request
from meow_contracts.forms import RentRequestForm, RentContractForm
from meow_main.db import has_privilege
from meow_main.views import UserViewMixin


class RentRequestCreateView(UserViewMixin, TemplateView):

    template_name = 'meow_contracts/create_or_edit_page.html'

    def get(self, request, **kwargs):
        context_data = self.get_context_data(**kwargs)
        token = request.COOKIES.get('token')
        if not has_privilege(token, 'create_rent_request'):
            raise Http404()

        context_data['form'] = RentRequestForm()
        return render(request, self.template_name, context=context_data)

    def post(self, request, **kwargs):
        form = RentRequestForm(request.POST)
        context = self.get_context_data(**kwargs)
        area_id = kwargs.get('area_id', None)
        tenant_id = get_tenant_id(request.COOKIES['token'])
        if tenant_id is None:
            raise Http404()

        if form.is_valid():
            created = create_rent_request(tenant_id, area_id, form.cleaned_data['description'])
            if created:
                return redirect('rent-request-list')
            else:
                pass
                # form.add_error('non_fields_errors', 'Failed to create shopping mall :C')

        context['form'] = form
        return render(request, self.template_name, context=context)


class RentRequestListView(UserViewMixin, TemplateView):

    template_name = 'meow_contracts/rent_request_list.html'

    def get(self, request, **kwargs):
        token = request.COOKIES.get('token', None)
        context = self.get_context_data(**kwargs)
        if context['user_group_name'] == 'tenants':
            tenant_id = get_tenant_id(token)
            if tenant_id < 0:
                raise Http404()
            context['rent_requests'] = get_tenant_rent_requests(tenant_id)
        else:
            landlord_id = get_landlord_id(token)
            if landlord_id < 0:
                raise Http404()
            context['rent_requests'] = get_landlord_rent_requests(landlord_id)
        return render(request, self.template_name, context=context)


class RentContractListView(UserViewMixin, TemplateView):

    template_name = 'meow_contracts/rent_contract_list.html'

    def get(self, request, **kwargs):
        token = request.COOKIES.get('token', None)
        context = self.get_context_data(**kwargs)
        if context['user_group_name'] == 'tenants':
            tenant_id = get_tenant_id(token)
            if tenant_id < 0:
                raise Http404()
            context['rent_contracts'] = get_tenant_rent_contracts(tenant_id)
        else:
            landlord_id = get_landlord_id(token)
            if landlord_id < 0:
                raise Http404()
            context['rent_contracts'] = get_landlord_rent_contracts(landlord_id)
        return render(request, self.template_name, context=context)


class DeleteRentContractView(UserViewMixin, TemplateView):

    def get(self, request, **kwargs):
        token = request.COOKIES.get('token', None)
        contract_id = kwargs.get('contract_id')
        landlord_id = get_landlord_id(token)
        if landlord_id < 0:
            raise Http404()
        result = delete_rent_contract(landlord_id, contract_id)
        if result < 0:
            raise Http404()
        return redirect('rent-contract-list')


class DeleteRentRequestView(UserViewMixin, TemplateView):

    def get(self, request, **kwargs):
        tenant_id = kwargs.get('tenant_id')
        area_id = kwargs.get('area_id')
        result = delete_rent_request(tenant_id, area_id)
        if result < 0:
            raise Http404()
        return redirect('rent-request-list')


class StartRentView(UserViewMixin, TemplateView):

    def get(self, request, **kwargs):
        token = request.COOKIES.get('token', None)
        contract_id = kwargs.get('contract_id')
        landlord_id = get_landlord_id(token)
        if landlord_id < 0:
            raise Http404()
        result = start_rent(landlord_id, contract_id)
        if result < 0:
            raise Http404()
        return redirect('rent-contract-list')


class EndRentView(UserViewMixin, TemplateView):

    def get(self, request, **kwargs):
        token = request.COOKIES.get('token', None)
        contract_id = kwargs.get('contract_id')
        landlord_id = get_landlord_id(token)
        if landlord_id < 0:
            raise Http404()
        result = end_rent(landlord_id, contract_id)
        if result < 0:
            raise Http404()
        return redirect('rent-contract-list')


class RentContractCreateView(UserViewMixin, TemplateView):

    template_name = 'meow_contracts/create_or_edit_page.html'

    def get(self, request, **kwargs):
        context_data = self.get_context_data(**kwargs)
        token = request.COOKIES.get('token')
        landlord_id = get_landlord_id(token)
        if landlord_id < 0:
            raise Http404()
        if not has_privilege(token, 'create_or_update_contract'):
            raise Http404()

        contract_id = kwargs.get('contract_id', None)
        if contract_id is not None:
            contract = get_rent_contract(landlord_id, contract_id)
            if contract is None:
                raise Http404()
            data = {
                'code': contract[1],
                'start_date': contract[2],
                'end_date': contract[3],
                'price': contract[4],
                'additional_payment': contract[5],
                'discount': contract[6],
                'checking_account': contract[7],
                'requirements': contract[8],
            }
            context_data['form'] = RentContractForm(data)
        else:
            context_data['form'] = RentContractForm()

        return render(request, self.template_name, context=context_data)

    def post(self, request, **kwargs):
        token = request.COOKIES.get('token')
        form = RentContractForm(request.POST)
        context = self.get_context_data(**kwargs)
        contract_id = kwargs.get('contract_id', None)
        area_id = kwargs.get('area_id', None)
        tenant_id = kwargs.get('tenant_id', None)
        landlord_id = get_landlord_id(token)
        if landlord_id < 0:
            raise Http404()
        if form.is_valid():
            delete_rent_request(tenant_id, area_id)
            created = create_rent_contract(contract_id, area_id, tenant_id, landlord_id, form.cleaned_data)
            if created:
                return redirect('rent-contract-list')
            else:
                pass

        context['form'] = form
        return render(request, self.template_name, context=context)
