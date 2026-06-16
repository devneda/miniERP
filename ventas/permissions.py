from rest_framework.permissions import BasePermission

class EsStaffOSoloLectura(BasePermission):
    """
    Acceso de lectura para cualquier usuario autenticado.
    Escritura (POST, PUT, PATCH, DELETE) solo para staff.
    """
    METODOS_SEGUROS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in self.METODOS_SEGUROS:
            return True
        return request.user.is_staff