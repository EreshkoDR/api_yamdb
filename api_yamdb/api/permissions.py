from rest_framework import permissions
from users.models import User


class IsAdminPermission(permissions.BasePermission):
    """Разрешения уровня `администратор`."""
    def has_permission(self, request, view):
        # Здесь по-другому не получилось написать выражение, т.к.
        # при обращении анонимным пользователем выражение
        # request.user.role вызывает ошибку, что у модели
        # "анонимный пользователь" нет поля role
        if request.user.is_authenticated:
            return (
                request.user.role == User.ADMIN
                or request.user.is_superuser
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.role == User.ADMIN
                or request.user.is_superuser
            )
        return False


class IsModeratorPermission(permissions.BasePermission):
    """Разрешения уровня `модератор`."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == User.MODERATOR
                or request.user.is_superuser
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.role == User.MODERATOR
                or request.user.is_superuser
            )
        return False


class IsUserPermission(permissions.BasePermission):
    """Разрешения уровня `авторизированный пользователь`."""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOrAdminPermission(permissions.BasePermission):
    """
    Настройки доступа к Жанрам,Произведениям.
    Полный доступ у администратора и суперпользователя
    Только чтение у гостя, пользователя, модератора.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == User.ADMIN
                or request.user.is_superuser
            )
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.role == User.ADMIN
                or request.user.is_superuser
            )
        return request.method in permissions.SAFE_METHODS


class ReadOrUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == User.USER
                    or request.user.role == User.ADMIN
                    or request.user.is_superuser)
        return request.method in permissions.SAFE_METHODS


class CommmentAndReviewPermission(permissions.BasePermission):
    """
    Настройки доступа к Комментариям и Отзывам:
    полный доступ для автора, администратора, суперюзера
    право на удаление и частичное изменение у модератора
    только чтение у гостя и зарегистрированного пользователя.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method == ('DELETE' or 'PATCH'):
                return (request.user.is_superuser
                        or request.user.role == User.ADMIN
                        or request.user.role == User.MODERATOR
                        or obj.author == request.user)
            return (request.user.is_superuser
                    or request.user.role == User.ADMIN
                    or obj.author == request.user)
        return (request.method in permissions.SAFE_METHODS)
