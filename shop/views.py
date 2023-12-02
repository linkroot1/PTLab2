from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.db.models import F


from .models import Product, Purchase, Config


# Create your views here.
def index(request):
    if Purchase.objects.all().distinct('product_id').count() == 2 and Config.objects.get(id=1).discount == False:
       Product.objects.all().update(price = F("price") * 0.6)
       Config.objects.all().update(discount = True)
       Config.objects.all().update(countProducts = Purchase.objects.all().count())
       print("Дали скидку")

    if Config.objects.get(id=1).countProducts != None and Config.objects.get(id=1).countProducts != 0 and Purchase.objects.all().count() > Config.objects.get(id=1).countProducts and Config.objects.get(id=1).discount == True:
       Product.objects.all().update(price = F("price") / 0.6)
       Config.objects.all().update(countProducts=0)
       print("Убрали скидку")

    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')

