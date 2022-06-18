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
    text = models.TextField(
        verbose_name='Posts text',
        help_text="Write what's on your mind?"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Posts date and time'
    )
    author = models.ForeignKey(User,
                               null=False,
                               on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Author')
    country = models.ForeignKey(Country,
                                null=True,
                                blank=False,
                                on_delete=models.SET_NULL,
                                related_name='posts',
                                verbose_name='Country about which post',
                                help_text='Choose a country')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.pk} | {self.author} | {self.text[:15]}'
