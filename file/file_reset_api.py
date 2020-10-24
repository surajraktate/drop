from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import boto3
from botocore.exceptions import NoCredentialsError

from mydataonline.utils import get_encrypted_decrypted_name
from file.models import FileData, File
from file.consumer_handler import get_file_data
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer

ACCESS_KEY = ''
SECRET_KEY = ''


class FileUploadAPI(APIView):
    parser_classes = (MultiPartParser,)

    def __init__(self):
        self.room_ip = ""
        self.room_name = ""

    def get(self, request):
        """
        this function is return all files
        :param request:
        :return:
        """
        list_of_file = get_file_data()
        return Response({"files": list_of_file}, status=200)

    def post(self, request):
        """
        this function is upload the file on s3 bucket
        :param request:
        :return:
        """
        file_obj = request.FILES['file']
        self.room_ip = request.META.get('REMOTE_ADDR')
        self.room_name = request.data.get("room_name")
        self.save_file_on_disk(file_obj)
        file_url = self.upload_to_aws(file_obj, 'cponlinedemo')
        return Response({"file_url": file_url}, status=200)

    def delete(self, request):
        """
        this function delete file from s3 and database
        :param request:
        :return:
        """
        pk = request.query_params.get("file_id")
        try:
            file_object = FileData.objects.get(pk=pk)
        except Exception as e:
            print("Error To delete file", e)
            return Response({"error": "Unable to delete file"}, status=400)
        else:

            file_object.delete()
            file_object.save()
            return Response(status=204)

    def get_aws_resource(self, resource_name):
        """
        this function return aws resource
        :param resource:
        :return:
        """
        session = boto3.Session(
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
        )
        resource = session.resource(resource_name)
        if resource:
            return resource

    def upload_to_aws(self, local_file, bucket):

        try:
            s3 = self.get_aws_resource("s3")
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

    def delete_file_from_s3(self, filename, bucket_name):
        """
        this function is use to delete files from s3
        :param filename:
        :param bucket_name:
        :return:
        """
        s3 = self.get_aws_resource("s3")
        obj = s3.Object("mybucket", "media/private/test.txt")
        obj.delete()

    def save_file_on_disk(self, file_obj):
        """
        this function use to store uploaded file in disk
        """
        file_url = ""
        return file_url


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """

        """
        self.room_ip = request.META.get('REMOTE_ADDR')
        self.room_name = request.data.get("room_name") if request.data.get("room_name") else None

        request_data = request.data

        try:
            request_data.update({"room_name": self.room_name, "room_ip": self.room_ip})
        except Exception as e:
            print("e")

        file_serializer = FileSerializer(data=request_data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        this function delete file from s3 and database
        :param request:
        :return:
        """
        try:
            file_object = File.objects.get(id=id)
        except Exception as e:
            print("Error To delete file", e)
            return Response({"error": "Unable to delete file"}, status=400)
        else:

            file_object.delete()
            return Response(status=204)

    def get(self, request, *args, **kwargs):
        """
        this function is return all files
        :param request:
        :return:
        """
        list_of_file = get_file_data()
        return Response({"files": list_of_file}, status=200)