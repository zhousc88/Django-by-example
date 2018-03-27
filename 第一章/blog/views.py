from django.shortcuts import render,get_object_or_404
from .models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView
# Create your views here.
def post_list(request):
    obj_list=Post.published.all()
    pagnator=Paginator(obj_list,3)
    page=request.GET.get('page')
    try:
        posts=pagnator.page(page)
    except PageNotAnInteger:
        posts=pagnator.page(1)
    except EmptyPage:
        posts=pagnator.page(pagnator.num_pages)
    return render(request,'blog/post/list.html',{'page':page,'posts':posts})

def post_detail(request,year,month,day,post):
    post1=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    return render(request,'blog/post/detail.html',{'post':post1})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'