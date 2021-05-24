from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse


class Rubric(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    slug = models.SlugField(null=True)
    title = models.CharField(_("Post title"), max_length=50)
    body = models.TextField()
    published = models.DateTimeField(auto_now=True)
    rubric = models.ForeignKey(to=Rubric, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, default=User.objects.get(username='admin').pk)

    def __str__(self):
        return f'{self.title} - {self.published.strftime("%d.%m.%Y %H:%M:%S")}'

    def get_absolute_url(self):
        # return reverse("_detail", kwargs={"pk": self.pk})
        pass

    class Meta:
        ordering = ['-published']
