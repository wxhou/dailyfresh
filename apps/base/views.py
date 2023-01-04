from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from drf_yasg.utils import swagger_auto_schema
from .models import UploadModel
from .serializers import UploadSerializer


# Create your views here.


class UploadAPIView(APIView):
    """文件上传"""
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(request_body=FileSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        obj = UploadModel.objects.filter(uniqueId=data['uniqueId'], is_deleted=False).first()
        if obj is None:
            obj = UploadModel.objects.create(**data, fileName=data['file'].name, uid=request.user)
        result = {"id": obj.id, "file": str(obj.file), "fileName": obj.fileName}
        return Response(result, status=status.HTTP_200_OK)
