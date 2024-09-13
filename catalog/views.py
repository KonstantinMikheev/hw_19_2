from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView

from catalog.forms import ContactForm, ProductForm, VersionForm
from catalog.models import Category, Product, ContactData, Version


class ProductListView(ListView):
    """Класс-контроллер для вывода главной страницы"""
    model = Product

    def get_queryset(self):
        """Метод для фильтрации продуктов по категории с подгрузкой версий"""
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        queryset = queryset.prefetch_related('versions')
        return queryset

    def get_context_data(self, **kwargs):
        """Метод для вывода названия версии если она активна"""
        context_data = super().get_context_data(**kwargs)
        context_data['categories'] = Category.objects.all()
        context_data['title'] = 'Главная'
        products = context_data['product_list']
        for product in products:
            active_version = Version.objects.filter(product_id=product.pk, version_flag=True)
            if active_version:
                product.active = active_version.last().version_name
            else:
                product.active = 'Нет активной версии'
        return context_data


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products_list')

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', args=[self.object.pk])

    def get_context_data(self, *args, **kwargs):
        """Метод для вывода формы версии при редактировании продукта"""
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        """Метод для сохранения продукта и версии при редактировании"""
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


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
        """Метод для отображения формы и списка контактов"""
        form = ContactForm()
        contacts_data = ContactData.objects.all()  # Получаем все контакты из базы данных
        return render(request, self.template_name, {
            'form': form,
            'contacts': contacts_data,
            'title': 'Контактная информация',
        })

    def post(self, request, *args, **kwargs):
        """Метод для обработки отправленной формы контактов"""
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
