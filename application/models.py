# coding=utf-8
from django.db import models

class Tag(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=u"Название"
    )

    slug = models.SlugField(
        max_length=200,
        verbose_name=u"Псевдоним",
        db_index=True,
        unique=True,
        help_text=u"Ипользуется для формирования ссылки на спиcок по тегам"
    )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        raise NotImplementedError # TODO Метод должен возвращать ссыку на публикации по тегу. Нужно для sitemaps.

    class Meta:
        verbose_name = u"Тег"
        verbose_name_plural = u"Теги"


class Publication(models.Model):
    TYPES = {
        0: u"Аналитика",
        1: u"Интервью",
        2: u"Новость/Акция",
    }
    cont_type = models.SmallIntegerField(
        choices=TYPES.items(),
        default=0,
        db_index=True,
        verbose_name=u"Тип публикации"
    )
    STATUSES = {
        0: u"Не опубликовано",
        1: u"Опубликовано",
        2: u"Черновик",
    }
    status = models.SmallIntegerField(
        choices=STATUSES.items(),
        default=1,
        verbose_name=u"Статус"
    )
    title = models.CharField(
        max_length=200,
        verbose_name=u"Название",
    )
    cover = FilerImageField(
        null=True,
        blank=True,
        verbose_name=u"Связанное изображение"
    )
    slug = models.SlugField(
        max_length=200,
        db_index=True,
        verbose_name=u"Псевдоним",
    )
    intro = HTMLField(
        null=True,
        blank=True,
        verbose_name=u"Введение",
    )
    content = HTMLField(
        null=True,
        blank=True,
        verbose_name=u"Содержимое",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u"Создана",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=u"Изменена",
    )
    created_by = models.ForeignKey(
        to=get_user_model(),
        db_index=True,
        null=True,
        blank=True,
        verbose_name=u"Автор",
        related_name='created_publications',
    )
    updated_by = models.ForeignKey(
        to=get_user_model(),
        null=True,
        blank=True,
        verbose_name=u"Последний раз изменял",
        related_name='updated_publications',

    )
    related_company = models.ForeignKey(
        to=Company,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=u"Компания",
        help_text=u"Компания, с которой связана публикация.",
        related_name='publications'
    )
    tags = models.ManyToManyField(
        to=Tag,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=u"Теги",
        related_name='publications'
    )
    seo_fields = GenericRelation(
        to=SeoInfo,
        db_index=True,
    )

    @property
    def tag_names(self):
        return u', '.join(t.title for t in self.tags.all())

    def get_type_str(self):
        return self.TYPES[self.cont_type]

    def get_type_slug_str(self):
        if self.cont_type == 0:
            return "analytics"
        elif self.cont_type == 1:
            return "interviews"
        else:
            return "news"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('publication_detail', kwargs={'material': self.my_type_str, 'pk': self.pk})

    class Meta:
        verbose_name = u"Публикация"
        verbose_name_plural = u"Публикации"
