from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from mysite import settings
from taggit.models import Tag
from django.db.models import Count
# Create your views here.
def post_list(request,tag_slug=None):
    obj_list=Post.published.all()
    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        obj_list=obj_list.filter(tags__in=[tag])
    pagnator=Paginator(obj_list,3)
    page=request.GET.get('page')
    try:
        posts=pagnator.page(page)
    except PageNotAnInteger:
        posts=pagnator.page(1)
    except EmptyPage:
        posts=pagnator.page(pagnator.num_pages)
    return render(request,'blog/post/list.html',{'page':page,'posts':posts,'tag':tag})

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)
    new_comment = None
    post_tags_ids=post.tags.values_list('id',flat=True)
    similar_posts=Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts=similar_posts.annotate(same_tag=Count('tags')).order_by('-same_tag','-publish')[:4]
    if request.method=='POST':
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
    else:
        comment_form=CommentForm()
    return render(request,'blog/post/detail.html',{'post':post,'comments':comments,'new_comment':new_comment,'comment_form':comment_form,'similar_posts':similar_posts})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request,post_id):
    sent = False
    post=get_object_or_404(Post,id=post_id,status='published')
    if request.method=='POST':
        form =EmailPostForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{} {} recommends you reading "{}"'.format(data['name'],data['email'],post.title)
            message='Read "{}" at {} \n\n{} comments: {}'.format(post.title,post_url,data['name'],data['comments'])
            send_mail(subject,message,settings.EMAIL_HOST_USER,[data['to']])
            sent=True
    else:
        form=EmailPostForm()

    return  render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})