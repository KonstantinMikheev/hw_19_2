from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

from catalog.forms import ContactForm
from catalog.models import Category, Product, ContactData


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        data['title'] = 'Главная'
        return data


class ProductDetailView(DetailView):
    model = Product


# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {'product': product}
#     return render(request, 'catalog/product_detail.html', context)


# def home(request):
#     # Получаем список всех категорий
#     categories = Category.objects.all()
#     category_id = request.GET.get('category')
#     if category_id:
#         products = Product.objects.filter(category_id=category_id)
#     else:
#         products = Product.objects.all()
#     context = {
#         'products': products,
#         'categories': categories,
#         'title': 'Главная',
#     }
#     return render(request, 'catalog/products.html', context)


class ContactsDataView(TemplateView):
    template_name = "catalog/contacts.html"

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        contacts_data = ContactData.objects.all()  # Получаем все контакты из базы данных
        return render(request, self.template_name, {
            'form': form,
            'contacts': contacts_data,
            'title': 'Контактная информация',
        })

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message")
            print(f'You have a new message from {name} ({phone}): {message}')
            ContactData.objects.create(name=name, phone=phone, message=message)
        contacts_data = ContactData.objects.all()
        return render(request, 'catalog/contacts.html', {'contacts': contacts_data, 'title': 'Контакты'})

# def contacts(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'You have a new message from {name} ({phone}): {message}')
#         ContactData.objects.create(name=name, phone=phone, message=message)
#     contacts_data = ContactData.objects.all()
#     return render(request, 'catalog/contacts.html', {'contacts': contacts_data, 'title': 'Контакты'})
