from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS

# Permission to get, update or delete a user or create one
class IsAuthenticatedAndOwnerUserOrCreateOne(IsAuthenticated):

  def has_permission(self, request, view):
    if request.method == 'POST':
      return True

    return super().has_permission(request, view)

  def has_object_permission(self, request, view, obj):
    return request.user == obj


# Permission to update or delete something which user is owner, or is authenticated to create an obj
class IsAuthenticatedAndOwnerUserOrReadOnly(IsAuthenticatedOrReadOnly):

  def has_object_permission(self, request, view, obj):
    if request.method in SAFE_METHODS:
      return True

    return request.user == obj
