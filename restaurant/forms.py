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


Dish_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddDishForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=Dish_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)