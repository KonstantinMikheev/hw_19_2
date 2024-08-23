from django.shortcuts import render

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
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name} ({phone}): {message}')
        ContactData.objects.create(name=name, phone=phone, message=message)
    contacts_data = ContactData.objects.all()
    return render(request, 'catalog/contacts.html', {'contacts': contacts_data})
