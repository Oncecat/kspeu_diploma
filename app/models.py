from django.db import models
from django.contrib.auth.models import User


class Myip(models.Model):
    class Meta:
        verbose_name = 'IP'
        verbose_name_plural = 'IP'
        ordering = ['id']

    TYPE_IP = (
        (0, 'Динамический'),
        (1, 'Статический'),
        (2, 'Не выбрано')
    )
    ip = models.CharField('IP', max_length=255, null=True, blank=True)
    mac = models.CharField('MAC', max_length=255)
    type = models.CharField('Тип', max_length=255, choices=TYPE_IP, default=2, null=True, blank=True)
    slug = models.SlugField('Slug', blank=True, null=True, max_length=50)
    description = models.CharField('Description', max_length=255, default='Без описания')

    def save(self, *args, **kwargs):
        # self.description = '{}'.format(str(self.description))
        self.slug = '{}'.format(str(self.ip))
        super(Myip, self).save()
   


    # def save_desc(self, *args, **kwargs):
    #     self.description = '{}'.format(str(self.description))
    #     super(Myip,self).save()