from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Permite operações de escrita somente para usuários staff(admin).
    Métodos de leitura (GET, HEAD, OPTIONS) estão liberados.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsCoordinatorOrAdminOrReadOnly(BasePermission):
    """
    Permite escrita somente para usuários com role 'coordinator' ou staff.
    É necessário que o modelo User tenha atributo `role`.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_staff or getattr(user, "role", None) == "coordinator")
        )


class IsObjectOwnerOrAdmin(BasePermission):
    """
    Permite update/delete somente se o usuário for o proprietário do objeto ou admin.
    Exige que o objeto tenha atributo `owner`.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and (request.user.is_staff or getattr(obj, "owner", None) == request.user)
        )
