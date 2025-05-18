from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _

from tree_menu.constants import MAX_NAME_LENGHT, MAX_URL_LENGHT


class MenuItem(models.Model):
    """Модель для хранения пунктов меню."""

    name = models.CharField(_('name'), max_length=MAX_NAME_LENGHT)
    named_url = models.CharField(
        _('Именованый URL'),
        max_length=MAX_URL_LENGHT,
        blank=True,
        help_text=_('Названный URL из файла urls.py')
    )
    url = models.CharField(
        _('url'),
        max_length=MAX_URL_LENGHT,
        blank=True,
        help_text=_('Абсолютный путь')
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Родительский элемент')
    )
    menu_name = models.CharField(
        _('Название меню'),
        max_length=MAX_NAME_LENGHT,
        help_text=_('Имя меню, к которому принадлежит элемент')
    )
    order = models.PositiveIntegerField(_('Порядок'), default=0)

    class Meta:
        verbose_name = _('Элемент меню')
        verbose_name_plural = _('Элементы меню')
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.named_url
        return self.url or '#'

    def is_active(self, current_path):
        item_url = self.get_url()
        if not item_url or item_url == '#':
            return False
        return current_path == item_url or current_path.startswith(item_url + '/')
