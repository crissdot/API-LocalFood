from rest_framework import permissions

# Permission to get, update or delete a user or creeate one
class IsAuthenticatedAndOwnerUserOrCreateOne(permissions.IsAuthenticated):

  def has_permission(self, request, view):
    if request.method == 'POST':
      return True

    return super().has_permission(request, view)

  def has_object_permission(self, request, view, obj):
    return request.user == obj
