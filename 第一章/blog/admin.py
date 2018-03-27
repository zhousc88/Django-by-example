from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status','created','publish','author')
    search_fields = ('title','body')
    prepopulated_fields = {'slug':('title',)}#标题来填充slug字段
    raw_id_fields = ('author',)#作者搜索控件
    date_hierarchy = 'publish'
    ordering = ['status','publish']
admin.site.register(Post,PostAdmin)