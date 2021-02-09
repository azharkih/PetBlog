from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Класс IsAuthorOrReadOnly используется для установки ограничений на изменение
    записей только их авторами.

    Родительский класс -- permissions.BasePermission.

    Методы класса
    --------
    has_object_permission(self, request, view, obj) -- определяет права на
    обработку объекта.
    """

    def has_object_permission(self, request, view, obj):
        """Определить и вернуть право на поступивший запрос."""
        return (request.method in permissions.SAFE_METHODS or
                obj.author == request.user)
