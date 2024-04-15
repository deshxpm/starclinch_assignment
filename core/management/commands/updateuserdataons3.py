from django.core.management.base import BaseCommand
from core.models import UserProfile
import csv
import boto3

class Command(BaseCommand):
    help = 'Update user data on Amazon S3'

    def handle(self, *args, **kwargs):
        # Fetch user data from the database
        users = UserProfile.objects.all()

        # Write user data to a CSV file
        csv_file_path = '/starclinch/csv/file.csv'
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['user_id', 'name', 'email', 'phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user in users:
                writer.writerow({'user_id': user.id, 'name': f'{user.first_name} {user.last_name}', 'email': user.email, 'phone': user.phone})

        # Upload the CSV file to Amazon S3
        s3 = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')
        bucket_name = 'your-bucket-name'
        s3.upload_file(csv_file_path, bucket_name, 'user_data.csv')

        self.stdout.write(self.style.SUCCESS('Successfully updated user data on Amazon S3'))
