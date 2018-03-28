from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from images.common.decorators import  ajax_required
from actions.utils import create_action
from django.conf import settings
import redis
r=redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

@login_required
def image_create(request):
    if request.method=='POST':
        form=ImageCreateForm(data=request.POST)
        if form.is_valid():
            img_data=form.cleaned_data
            new_item=form.save(commit=False)
            new_item.user=request.user
            new_item.save()
            messages.success(request,'Image added successfully')
            return redirect(new_item.get_absolute_url())
    else:
        form =ImageCreateForm(data=request.GET)
    return  render(request,'images/image/create.html',{'section':'image',
                                                      'form':form})

def image_detail(request,id,slug):
    image=get_object_or_404(Image,id=id,slug=slug)
    total_views=r.incr('image:{}:views'.format(image.id))
    r.zincrby('image_ranking',image.id,1)
    return render(request,'images/image/detail.html',
    {'section':'image','image':image,'total_views':total_views})

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id=request.POST.get('id')
    action =request.POST.get('action')
    if image_id and action:
        try:
            image=Image.objects.get(id=image_id)
            if action=='like':
                image.user_like.add(request.user)#多对多，传递不存在，操作不进行
                create_action(request.user,"like",image)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return  JsonResponse({'status':'ko'})

@login_required
def image_list(request):
    images=Image.objects.all().order_by('pk')
    paginator=Paginator(images,8)
    page=request.GET.get('page')
    try:
        images=paginator.page(page)
    except PageNotAnInteger:
        images=paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images=paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,'images/image/list_ajax.html',
                      {'section':'images','images':images})
    return  render(request,'images/image/list.html',
                   {'section':'images','images':images})

@login_required
def image_ranking(request):
    image_ranking=r.zrange('image_ranking',0,-1,desc=True)[:10]
    image_ranking_ids=[int(id) for id in  image_ranking]
    most_viewed=list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x:image_ranking_ids.index(x.id))
    return  render(request,'images/image/ranking.html',
                   {'section':'images','most_viewed':most_viewed})




