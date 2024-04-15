import csv
import os
import boto3
from django.conf import settings
from celery import shared_task
from core.models import UserProfile

@shared_task
def update_user_data_on_s3():
    users = UserProfile.objects.all()

    csv_file_path = os.path.join(settings.BASE_DIR, 'user_data.csv')

    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['user_id', 'name', 'email', 'phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow({
                'user_id': user.id,
                'name': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'phone': user.phone
            })

    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = 'your-bucket-name'
    s3.upload_file(csv_file_path, bucket_name, 'user_data.csv')
