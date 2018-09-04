from rest_framework import permissions


class IsGetRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == "GET"
