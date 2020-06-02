from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import boto3
from botocore.exceptions import NoCredentialsError
from file.models import FileData
ACCESS_KEY = 'AKIAJM3VGNB46N6C3HLA'
SECRET_KEY = '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'


class FileUploadAPI(APIView):
    parser_classes = (MultiPartParser,)

    def __init__(self):
        self.room_ip = ""
        self.room_name = ""

    def post(self, request):
        file_obj = request.FILES['file']
        self.room_ip = request.META.get('REMOTE_ADDR')
        self.room_name = request.data.get("room_name")
        # do some stuff with uploaded file
        file_url = self.upload_to_aws(file_obj, 'cponlinedemo')
        return Response({"file_url": file_url}, status=200)

    def upload_to_aws(self, local_file, bucket):

        try:
            session = boto3.Session(
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
            )
            s3 = session.resource('s3')
            file_name = local_file.name.replace(" ", "_")
            s3.Bucket(bucket).put_object(Key='media/%s' % file_name, Body=local_file)
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
        else:
            print("Upload Successful")

            file_url = "https://%s.s3.us-east-2.amazonaws.com/media/%s" % (bucket, file_name)
            try:
                file_models_obj = FileData(room_ip=self.room_ip, room_name=self.room_name, file_url=file_url)
            except Exception as e:
                print("Error while updating database ", e)
            else:
                file_models_obj.save()

            return file_url

