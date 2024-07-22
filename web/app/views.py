from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
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
                serializer = self.serializer_class(data={'file': uploaded_file})

                if serializer.is_valid():
                    file_obj = serializer.save()
                    file_objs.append(file_obj)

                    try:
                        process_file.delay(file_obj.id)
                    except:
                        file_obj.delete()
                        return Response({'error': 'Ошибка при запуске асинхронной задачи.'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer = FileSerializer(file_objs, many=True)

            response_data = {
                'files': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        elif request.method == 'GET':
            return render(request, 'app/upload_form.html')


class CustomApiRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'files': reverse('file-list', request=request, format=kwargs.get('format')),
            'files-upload': reverse('file-upload', request=request, format=kwargs.get('format')),
        })
