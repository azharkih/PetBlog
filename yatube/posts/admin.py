from django.contrib import admin
from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    """ Класс PostAdmin используется для конфигурации отображения модели Post
    в админ-панели

    Атрибуты класса
    --------
    list_display : Tuple[str]
        Список отображаемых полей
    search_fields : Tuple[str]
        Список полей по которым осуществляется поиск
    list_filter : Tuple[str]
        Список полей по которым может применен фильтр
    empty_value_display : str
        Значение отображаемое вместо пустой строки.
    """

    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    """ Класс GroupAdmin используется для конфигурации отображения модели Group
    в админ-панели

    Атрибуты класса
    --------
    list_display : Tuple[str]
        Список отображаемых полей
    search_fields : Tuple[str]
        Список полей по которым осуществляется поиск
    empty_value_display : str
        Значение отображаемое вместо пустой строки.
    """

    list_display = ('slug', 'title', 'description')
    search_fields = ('title', 'description',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
