from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza
from django.shortcuts import get_object_or_404, redirect
def home(request):
    return render(request, 'pizza/home.html', {})

def order(request):
    multiple_form = MultiplePizzaForm()

    if request.method == 'POST':
        # Fixed typo: PizzaFrom should be PizzaForm
        filled_form = PizzaForm(request.POST, request.FILES)
        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            note = 'Thanks For Ordering! Your %s %s and %s is on its way.' % (
                filled_form.cleaned_data['size'],
                filled_form.cleaned_data['topping1'],
                filled_form.cleaned_data['topping2'],
            )
            # Reset form after order submission
            new_form = PizzaForm()
            return render(request, 'pizza/order.html', {'created_pizza_pk':created_pizza_pk,'PizzaForm': new_form, 'note': note, 'multiple_form': multiple_form})

    else:
        form = PizzaForm()  # Fixed typo: PizzaFrom should be PizzaForm
        return render(request, 'pizza/order.html', {'PizzaForm': form, 'multiple_form': multiple_form})

def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)

    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']

    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note = 'Pizzas have been ordered!'
        else:
            note = 'Order not created. Please try again.'
        return render(request, 'pizza/pizzas.html', {'note': note, 'formset': filled_formset})  # Use filled_formset here
    else:
        formset = PizzaFormSet()  # Create a new formset for GET requests
        return render(request, 'pizza/pizzas.html', {'formset': formset})

def edit_order(request, pk):
    # Fetch the pizza object or return a 404 if not found
    pizza = get_object_or_404(Pizza, pk=pk)
    form = PizzaForm(instance=pizza)

    if request.method == 'POST':
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = 'Order Updated'
            return render(request, 'pizza/edit_order.html', {'pizzaform': form, 'pizza': pizza,'note':note})

                # Redirect to a success page or the pizzas list page
            # Make sure to define a URL name for the redirection

    return render(request, 'pizza/edit_order.html', {'pizzaform': form, 'pizza': pizza})
