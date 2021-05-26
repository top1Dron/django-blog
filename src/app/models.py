from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy


class Rubric(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUSES = (
        ('OM', 'On moderation'),
        ('PB', 'Published'),
        ('FB', 'Forbidden')
    )


    slug = models.SlugField(null=True)
    title = models.CharField(_("Post title"), max_length=50)
    body = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    rubric = models.ForeignKey(to=Rubric, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, default=User.objects.get(username='admin').pk)
    status = models.CharField(max_length=2, choices=STATUSES, default='OM')
    

    def __str__(self):
        return f'{self.title} - {self.published.strftime("%d.%m.%Y %H:%M:%S")}'

    def get_absolute_url(self):
        # return reverse("_detail", kwargs={"pk": self.pk})
        pass

    class Meta:
        ordering = ['-published']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    body = models.TextField()
    published = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.author.username}-{self.post.title}-{self.body}'

    class Meta:
        ordering = ['-published']

    @property
    def get_delete_url(self):
        return reverse_lazy('app:delete_comment', kwargs={'slug': self.post.slug, 'pk': self.pk})
