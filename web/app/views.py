from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import File
from .serializers import FileSerializer
from .tasks import process_file


class FileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    @action(detail=False, methods=['post', 'get'])
    def upload(self, request):
        if request.method == 'POST':
            files = request.FILES.getlist('file')
            file_objs = []

            for uploaded_file in files:
                file_obj = File(file=uploaded_file)
                file_obj.save()
                file_objs.append(file_obj)

                process_file.delay(file_obj.id)

            serializer = FileSerializer(file_objs, many=True)

            response_data = {
                'files': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        elif request.method == 'GET':
            return render(request, 'app/upload_form.html')
