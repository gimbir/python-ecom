from mptt.fields import TreeForeignKey
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel
from django.db import models
from django.urls import reverse


# Create your models here.
class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayir')
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        # level_attr = 'mptt_level'
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(upload_to='images/',null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount=models.IntegerField(default=0)
    detail=models.TextField()
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"'.format(self.image.url))
    image_tag.short_description = 'Image'

class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"'.format(self.image.url))
    image_tag.short_description = 'Image'

    