from django.shortcuts import render,redirect,get_object_or_404
from .models import  OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .task import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],
                                         price=item['price'],quantity=item['quantity'])
            cart.clear()
            #order_created(order.id)
            cart.session['order_id']=order.id
           # request.sesssion['order_id']=order.id
            #return  render(request,'orders/order/created.html',{'order':order})
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return  render(request,'orders/order/create.html',{'cart':cart,'form':form})

@staff_member_required
def admin_order_detaill(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    return render(request,'admin/orders/order/detail.html',{'order':order})

@staff_member_required
def admin_order_pdf(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    html = render_to_string('orders/order/pdf.html',{'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Dispostion'] = 'filename="order_{}.pdf"'.format(order_id)
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(
        settings.STATIC_ROOT + 'css/pdf.css')])
    return response
