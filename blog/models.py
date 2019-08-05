from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title= models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    summary = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to='img', blank=True)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']
        def __unicode__(self):
            return u'%s'% self.title

    def get_absolute_url(self):
        return reverse('blog:blog', args=[self.slug])