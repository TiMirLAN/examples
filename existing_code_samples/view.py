from django.core.urlresolvers import reverse
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
import json

__author__ = 'timirlan'


class OrderFormView(FormView):
    form_class = OrderFormView
    template_name = 'orders/form.html'

    def dispatch(self, request, *args, **kwargs):
        if (not request.user.is_authenticated()) or request.user.profile.is_translator:
            return HttpResponseForbidden()
        return super(OrderFormView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(OrderFormView, self).get_form_kwargs()
        if 'pk' in self.kwargs:
            kwargs['instance'] = get_object_or_404(Order, pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        order = form.save()
        order.customer.add_rating('create_new_order')
        if form.payment_total > 0:
            robokassa_order = RobokassaOrder.objects.create(
                owner=self.request.user,
                sum=form.payment_total,
                payload=json.dumps(dict(
                    order=order.pk,
                    enable=form.payments_opts
                ))
            )
            robokassa_order.actions.add(
                *list(RobokassaAction.objects.filter(sid__in=form.payments_opts))
            )
            self.success_url = reverse('billing:commit_exact_order', kwargs=dict(pk=robokassa_order.pk))
        else:
            self.success_url = reverse("orders:detailed_view", kwargs=dict(pk=order.pk))
        return super(OrderFormView, self).form_valid(form)