def get_data_with_new_field(request, field_name, field_value):
  data = request.data.copy()
  data[field_name] = field_value
  return data
