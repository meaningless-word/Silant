from rest_framework import permissions
from accounts.models import User


class MaintenancePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, User.SERVICE_COMPANY, User.CLIENT, ]
        if view.action in ['create', 'update', 'partial_update', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, User.SERVICE_COMPANY, User.CLIENT, ]
        if view.action in ['destroy', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, ]  
    
    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, User.SERVICE_COMPANY, User.CLIENT, ]
        if view.action in ['create', 'update', 'partial_update', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, User.SERVICE_COMPANY, User.CLIENT, ]
        if view.action in ['destroy', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, ]
        
class ClaimPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, User.SERVICE_COMPANY, User.CLIENT, ]
        if view.action in ['create', 'update', 'partial_update', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, User.SERVICE_COMPANY, ]
        if view.action in ['destroy', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, ]
    
    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, User.SERVICE_COMPANY, User.CLIENT, ]
        if view.action in ['create', 'update', 'partial_update', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, User.SERVICE_COMPANY, ]
        if view.action in ['destroy', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, ]


class MachinePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, User.SERVICE_COMPANY, User.CLIENT, ]
        if view.action in ['create', 'update', 'partial_update', 'destroy', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, ]
    
    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, User.SERVICE_COMPANY, User.CLIENT, ]
        if view.action in ['create', 'update', 'partial_update', 'destroy', ]:
            return request.user.is_authenticated and request.user.role in [User.MANAGER, ]