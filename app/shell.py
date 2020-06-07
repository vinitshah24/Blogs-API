import json
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from blogs.api.serializers import BlogsSerializer
from blogs.models import Blogs as BlogsModel

# Individual Object Serialization
obj = BlogsModel.objects.first()
indv_ser = BlogsSerializer(obj)
indv_ser.data
bytes_data = JSONRenderer().render(indv_ser.data)
json_data = json.loads(bytes_data)
print(json_data)

# List
qs = BlogsModel.objects.all()
list_ser = BlogsSerializer(qs, many=True)
list_ser.data
bytes_data2 = JSONRenderer().render(list_ser.data)
json_data2 = json.loads(bytes_data2)
print(json_data2)

# Insert
data = {'user': 1, 'content': 'Shell Insert!', 'image': None}
insert_ser = BlogsSerializer(data=data)
insert_ser.is_valid()
insert_ser.save()

# Update
obj = BlogsModel.objects.first()
data = {'content': 'Updated from shell', "user": 1}
update_ser = BlogsSerializer(obj, data=data)
update_ser.is_valid()
updated_obj = update_ser.save()
print(f"Updated ID #{updated_obj.id} : {updated_obj.content}")

# Delete
obj = BlogsModel.objects.last()
deleted_obj = obj.delete()
print(deleted_obj)  # tuple
