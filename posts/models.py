from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Country(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,
                               null=False,
                               on_delete=models.CASCADE,
                               related_name='posts')
    country = models.ForeignKey(Country,
                                null=True,
                                blank=False,
                                on_delete=models.SET_NULL,
                                related_name='posts')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.pk} | {self.author} | {self.text[:15]}'
