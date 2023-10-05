from django.shortcuts import render
from writers.serializers import Serializer, SerializerWriter
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from writers.models import Writer
from rest_framework.parsers import JSONParser

# Create your views here.

@csrf_exempt
def writers(request):
    writers = Writer.objects.all()
    serializer = Serializer(writers, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def writer(requset, pk):
    try:
        writer = Writer.objects.get(pk=pk)
    except Writer.DoesNotExist:
        return HttpResponse('Not found')

    if requset.method == 'GET':
        serializer = Serializer(writer)
        return JsonResponse(serializer.data,safe=False)
    elif requset.method == 'PUT':
        data = JSONParser().parse(requset)
        serializer = SerializerWriter(Writer, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse('{"state":"error"}')
    elif requset.method == 'DELETE':
        writer.delete()
        return HttpResponse(status=204)

def add(requset):
    if requset.method == 'POST':
        writer = Serializer(data=JSONParser().parse(requset))
        print(Serializer.data)
        writer.save()
    else:
        return HttpResponse('there are error')