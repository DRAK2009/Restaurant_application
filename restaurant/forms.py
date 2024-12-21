from django import forms

class DishFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ("", "Все"),
        ("salats", "Салати"),
        ("drinks", "Напої"),
        ("desserts", "Десерти"),
        ("meat", "М'ясо"),
        ("fast food", "Фаст Фуд"),
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label="Категорії")


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)