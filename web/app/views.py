from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from .models import File
from .serializers import FileSerializer


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

            for uploaded_file in files:
                # Создаем и сохраняем объект File для каждого файла
                file_obj = File(file=uploaded_file)
                file_obj.save()

            return HttpResponseRedirect('/files/')


        elif request.method == 'GET':
            # Возвращаем HTML-форму для загрузки файлов
            return render(request, 'app/upload_form.html')
