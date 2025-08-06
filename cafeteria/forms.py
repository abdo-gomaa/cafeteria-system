from django import forms
from .models import Order, OrderItem
from django.forms.models import inlineformset_factory
from cafeteria.models import MenuItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone_number', 'address', 'payment_method']
        widgets = {
            'customer_name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={
                'rows': 1,
                'style': 'resize: none; overflow: hidden;',
                'placeholder': 'Enter your address',
                'oninput': 'autoResize(this)'
            }),
        }

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=('item', 'quantity'),
    extra=1,  
    can_delete=True  
)

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        menu_items = MenuItem.objects.all()
        self.fields['item'].queryset = menu_items
        self.fields['item'].widget.attrs.update({'onchange': 'updateTotal()', 'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'oninput': 'updateTotal()', 'class': 'form-control'})