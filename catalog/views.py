from django.shortcuts import render, get_object_or_404

from catalog.models import Category, Product, ContactData


def home(request):
    # Получаем список всех категорий
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'title': 'Главная',
    }
    return render(request, 'catalog/products.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have a new message from {name} ({phone}): {message}')
        ContactData.objects.create(name=name, phone=phone, message=message)
    contacts_data = ContactData.objects.all()
    return render(request, 'catalog/contacts.html', {'contacts': contacts_data, 'title': 'Контакты'})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)
