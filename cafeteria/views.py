from django.shortcuts import render, redirect
from .models import MenuItem, Category
from .forms import OrderForm, OrderItemFormSet
from django.db import transaction

def menu_list(request):
    categories = Category.objects.all()
    menu_by_category = {}

    for category in categories:
        items = MenuItem.objects.filter(category=category, available=True)
        menu_by_category[category] = items

    return render(request, 'cafeteria/menu.html', {
        'menu_by_category': menu_by_category
    })

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST or None)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                order = form.save()
                formset.instance = order
                formset.save()
            return redirect('menu')
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, 'cafeteria/order_form.html', {'form': form, 'formset': formset})