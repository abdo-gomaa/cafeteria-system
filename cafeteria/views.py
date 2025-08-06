from django.shortcuts import render, redirect , get_object_or_404
from .models import MenuItem, Category , Order ,OrderItem
from .forms import OrderForm, OrderItemFormSet
from django.db import transaction
from django.utils import timezone
from django.utils.timezone import now,timedelta
from django.http import HttpResponseForbidden
from django.http import JsonResponse


def menu_list(request):
    categories = Category.objects.all()
    menu_by_category = {}
    for category in categories:
        items = MenuItem.objects.filter(category=category, available=True)
        menu_by_category[category] = items

    last_order = None
    add_allowed = False
    order_id = request.session.get('last_order_id')

    if order_id:
        try:
            last_order = Order.objects.get(id=order_id)
            if now() - last_order.created_at <= timedelta(minutes=20):
                add_allowed = True
        except Order.DoesNotExist:
            pass

    return render(request, 'cafeteria/menu.html', {
        'menu_by_category': menu_by_category,
        'last_order': last_order,
        'add_allowed': add_allowed
    })


def place_order(request):
    menu_items = MenuItem.objects.filter(available=True)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        item_ids = request.POST.getlist('item')
        quantities = request.POST.getlist('quantity')
        payment_method = request.POST.get('payment_method')

        card_number = request.POST.get('card_number') if payment_method == 'visa' else None
        card_name = request.POST.get('card_name') if payment_method == 'visa' else None
        expiry_date = request.POST.get('expiry_date') if payment_method == 'visa' else None
        cvv = request.POST.get('cvv') if payment_method == 'visa' else None

        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.payment_method = payment_method
                if payment_method == 'visa':
                    order.card_number = card_number
                    order.card_name = card_name
                    order.expiry_date = expiry_date
                    order.cvv = cvv
                order.save()
                for item_id, qty in zip(item_ids, quantities):
                    item = MenuItem.objects.get(pk=item_id)
                    OrderItem.objects.create(order=order, item=item, quantity=qty)
                request.session['last_order_id'] = order.id
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'cafeteria/order_form.html', {
        'form': form,
        'menu_items': menu_items
    })

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'cafeteria/order_detail.html', {
        'order': order
    })

def add_to_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    time_difference = now() - order.created_at

    if time_difference > timedelta(minutes=20):
        return render(request, 'cafeteria/too_late.html', {
            'order': order,
            'message': "YOU CAN'T ADD AFTER 20 MINUTES"
        })

    if request.method == 'POST':
        item_ids = request.POST.getlist('item')
        quantities = request.POST.getlist('quantity')

        for item_id, qty in zip(item_ids, quantities):
            item = MenuItem.objects.get(pk=item_id)
            OrderItem.objects.create(order=order, item=item, quantity=qty)

        return redirect('order_detail', order_id=order.id)

    menu_items = MenuItem.objects.filter(available=True)
    return render(request, 'cafeteria/add_to_order.html', {
        'order': order,
        'menu_items': menu_items
    })




def check_add_time(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        time_diff = timezone.now() - order.created_at
        allowed = time_diff <= timedelta(minutes=20)
        return JsonResponse({'allowed': allowed})
    except Order.DoesNotExist:
        return JsonResponse({'allowed': False})