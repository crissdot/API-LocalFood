def get_data_with_user_from_token(request, field):
  data = request.data.copy()
  data[field] = request.user.id
  return data
