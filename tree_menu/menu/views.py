from django.views.generic import DetailView, TemplateView
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class ServicesView(TemplateView):
    template_name = 'services.html'


class ProductsView(TemplateView):
    template_name = 'products.html'


def product_detail(request, product_id):
    return render(request, 'product_detail.html', {'product_id': product_id})


class CategoryView(DetailView):
    template_name = 'category.html'

    def get_object(self, queryset=None):
        return {'category_id': self.kwargs['category_id']}
