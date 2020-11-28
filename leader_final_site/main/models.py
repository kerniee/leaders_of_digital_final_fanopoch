from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    parent_name = models.CharField(max_length=255, verbose_name='Отчество', blank=True)


class ConjunctiveGroup(models.Model):
    groups = models.ManyToManyField(Group)


class CardType(models.Model):
    name = models.CharField(max_length=255)


class Card(models.Model):
    PRIORITIES = [
        (1, 'Низкий'),
        (2, 'Средний'),
        (3, 'Высокий')
    ]
    CARD_CLASSES = [
        (1, 'Постоянное поручение'),
        (2, 'Информационное сообщение'),
        (3, 'Поручение')
    ]

    header = models.CharField(max_length=255, verbose_name='Заголовок')
    cls = models.IntegerField(choices=CARD_CLASSES, verbose_name='Класс поручения')
    type = models.ForeignKey(CardType, on_delete=models.CASCADE, verbose_name='Тип поручения')
    priority = models.IntegerField(choices=PRIORITIES, verbose_name='Приоритет')

    deadline = models.DateTimeField(blank=True, null=True, verbose_name='Срок исполнения')
    is_finished = models.BooleanField(default=False, blank=True, verbose_name='Завершено?')
    finished_at = models.DateTimeField(blank=True, null=True, verbose_name='Фактический срок исполнения')

    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель',
                                related_name='my_cards', related_query_name='my_card')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    views = models.ManyToManyField(User, related_name='cards_viewed', related_query_name='card_viewed',
                                   verbose_name='Просмотрено?')

    to_users = models.ManyToManyField(User, related_name='assigned_cards', related_query_name='assigned_card')
    to_groups = models.ManyToManyField(ConjunctiveGroup)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки'


class Reply(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    text = models.TextField()


class Attachment(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments')
