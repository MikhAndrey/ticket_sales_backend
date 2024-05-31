import os
import uuid

from ticket_sales_backend import settings


def handle_uploaded_file(file, folder_name):
    upload_dir = str(os.path.join(settings.MEDIA_ROOT, folder_name))
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    ext = file.name.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return os.path.join(folder_name, filename)
