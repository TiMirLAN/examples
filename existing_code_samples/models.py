# coding=utf-8
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
__author__ = 'timirlan'


class CountedManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return super(CountedManager, self).get_query_set().filter(is_counted=True)


class RatingEvent(models.Model):
    #FIELDS
    EVENTS = tuple((name, name) for name in RATING_EVENTS_PRICES.keys())
    event_name = models.CharField(
        choices=EVENTS,
        max_length=50,
        db_index=True,
    )
    initiator_user = models.ForeignKey(
        to=get_user_model(),
        db_index=True,
        blank=True,
        null=True
    )
    additional_info = models.TextField(
        null=True,
        blank=True
    )
    modifier = models.IntegerField()
    is_counted = models.BooleanField(
        db_index=True,
        default=True,
    )
    #content type fields
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    #MANAGERS
    objects = models.Manager()
    counted = CountedManager()

    class Meta:
        index_together = (
            ('content_type', 'object_id'),
        )


class RatedModel(models.Model):
    rating_counter = models.BigIntegerField(
        db_index=True,
        default=0,
    )

    def add_rating(self, event_name, initiator=None, value=None):
        price = RATING_EVENTS_PRICES[event_name]
        if value:
            if isinstance(price, dict):
                if value < price['from'] or value > price['to']:
                    raise ValueError('value %d not in range [%d,%d]' % (value, price['from'], price['to']))
            modifier = value
        else:
            modifier = price

        RatingEvent.objects.create(
            event_name=event_name,
            modifier=modifier,
            content_object=self,
            initiator_user=initiator
        )
        if event_name in SUPPLANTED_EVENTS:
            RatingEvent.objects.filter(
                event_name=event_name,
                content_object=self,
                initiator_user=initiator,
            ).update(is_counted=False)
        self.update_rating()

    def update_rating(self):
        if self.pk:
            model_content_type = ContentType.objects.get_for_model(self.__class__)
            self.rating_counter = \
                RatingEvent.counted.filter(content_type=model_content_type, object_id=self.pk).aggregate(
                    models.Sum('modifier')
                )['modifier__sum']
            self.save()
            return True
        return False

    @property
    def rating(self):
        return self.rating_counter

    class Meta:
        abstract = True
