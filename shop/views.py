from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.db.models import F


from .models import Product, Purchase

# Create your views here.
def index(request):
    #ToDo: тут надо добавить еще условие что если у записей поле discount false то применяем скидку и меняем значение поля объектов на true
    if Purchase.objects.all().count() == 2 and Purchase.objects.get(id=1).discount == 0:
        Product.objects.all().update(price = F("price") * 0.6)

    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')

