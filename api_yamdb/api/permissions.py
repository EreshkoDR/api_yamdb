from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """Разрешения уровня `администратор`."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        return False


class IsModeratorPermission(permissions.BasePermission):
    """Разрешения уровня `модератор`."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == 'moderator'
                or request.user.is_superuser
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.role == 'moderator'
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
    """Разрешения уровня `аноним`."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        return request.method in permissions.SAFE_METHODS


class ReadOrUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == 'user'
                    or request.user.role == 'admin'
                    or request.user.is_superuser)
        return request.method in permissions.SAFE_METHODS


""" Настройки доступа к Комментариям и Отзывам:
полный доступ для автора, администратора, суперюзера
право на удаление и частичное изменение у модератора
только чтение у гостя и зарегистрированного пользователя. """


class CommmentAndReviewPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method == ('DELETE' or 'PATCH'):
                return (request.user.is_superuser
                        or request.user.role == 'admin'
                        or request.user.role == 'moderator'
                        or obj.author == request.user)
            return (request.user.is_superuser
                    or request.user.role == 'admin'
                    or obj.author == request.user)
        return (request.method in permissions.SAFE_METHODS)
