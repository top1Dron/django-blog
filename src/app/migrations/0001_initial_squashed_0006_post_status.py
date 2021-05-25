# Generated by Django 3.2.3 on 2021-05-25 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('app', '0001_initial'), ('app', '0002_auto_20210522_2342'), ('app', '0003_auto_20210524_1032'), ('app', '0004_post_author'), ('app', '0005_auto_20210525_1431'), ('app', '0006_post_status')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(null=True)),
                ('title', models.CharField(max_length=50, verbose_name='Post title')),
                ('body', models.TextField()),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('rubric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.classification')),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('status', models.CharField(choices=[('OM', 'On moderation'), ('PB', 'Published'), ('FB', 'Forbidden')], default='OM', max_length=2)),
            ],
            options={
                'ordering': ['-published'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('published', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.post')),
            ],
            options={
                'ordering': ['-published'],
            },
        ),
    ]