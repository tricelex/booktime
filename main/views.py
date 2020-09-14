from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import FormView
from main import forms, models


# Create your views here.
class ContactUsView(FormView):
    template_name = "contact_form.html"
    form_class = forms.ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(self)


class ProductListView(ListView):
    template_name = 'main/product_list.html'
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        if tag != 'all':
            self.tag = get_object_or_404(
                models.ProductTag, slug=tag
            )
        if self.tag:
            products = models.Product.objects.active().filter(tags=self.tag)
        else:
            products = models.Product.objects.active()
        return products.order_by('name')
