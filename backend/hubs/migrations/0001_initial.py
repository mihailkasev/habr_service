# Generated by Django 4.2.7 on 2023-12-05 07:22

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('link', models.URLField(unique=True, verbose_name='ссылка')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='заголовок')),
                ('body', models.TextField(verbose_name='содержание статьи')),
                ('published_at', models.DateTimeField(verbose_name='дата публикации статьи')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('link', models.URLField(unique=True, verbose_name='ссылка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='никнейм')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Hub',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('link', models.URLField(unique=True, verbose_name='ссылка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='название')),
                ('parse_period', models.PositiveSmallIntegerField(verbose_name='периодичность запроса хаба в мин.')),
            ],
            options={
                'verbose_name': 'Хаб',
                'verbose_name_plural': 'Хабы',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
                ('hub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='hubs.hub', verbose_name='избранный хаб')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
