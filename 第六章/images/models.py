from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Image(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,
                           related_name='images_created',
                           on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    slug=models.CharField(max_length=200,blank=True)
    url=models.URLField()
    image=models.ImageField(upload_to='image/%y/%m/%d')
    description=models.TextField(blank=True)
    created=models.DateField(auto_now_add=True,db_index=True)
    user_like=models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='images_liked',blank=True)
    total_like=models.PositiveIntegerField(db_index=True,default=0)

    def __str__(self):
        return  self.title

    def get_absolute_url(self):
        return reverse('images:detail',args=(self.id,self.slug))

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Image,self).save(*args,**kwargs)
