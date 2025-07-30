# core/forms.py
from django import forms
from .models import Transaction, Category

# Form for adding/editing a Transaction
class TransactionForm(forms.ModelForm):
    # Override the category field to be a ModelChoiceField
    # This allows us to filter categories based on the current user in the view
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(), # Start with an empty queryset
        required=False, # Category can be optional
        empty_label="Select a Category (Optional)",
        widget=forms.Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-purple-500'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-purple-500'}),
        initial=forms.DateField().widget.value_from_datadict(forms.DateField().widget.get_context(name='date', value=None, attrs={})['widget'], {}, 'date') # Set initial date to today
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-purple-500', 'placeholder': 'e.g., 500.00'})
    )
    transaction_type = forms.ChoiceField(
        choices=Transaction.TRANSACTION_TYPES,
        widget=forms.Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-purple-500'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-purple-500', 'rows': 3, 'placeholder': 'Optional description for the transaction'})
    )

    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'date', 'category', 'description']
        # We'll set the 'user' field in the view, not directly in the form

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # Pop the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Filter categories to only show those belonging to the current user
            self.fields['category'].queryset = Category.objects.filter(user=user)
        # Add Tailwind classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['category', 'date', 'amount', 'transaction_type', 'description']: # Already styled above
                field.widget.attrs['class'] = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-purple-500'


# Form for adding/editing a Category
class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-purple-500', 'placeholder': 'e.g., Groceries, Salary'})
    )

    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-purple-500'

    # Custom validation to ensure category name is unique per user
    def clean_name(self):
        name = self.cleaned_data['name']
        user = self.instance.user if self.instance.pk else self.initial.get('user') # Get user from instance or initial data
        if not user:
            raise forms.ValidationError("User must be provided for category validation.")

        # Check if a category with this name already exists for this user
        if Category.objects.filter(user=user, name__iexact=name).exists():
            raise forms.ValidationError("You already have a category with this name.")
        return name
