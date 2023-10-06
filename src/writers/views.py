from django.shortcuts import render
from writers.serializers import Serializer, SerializerWriter
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from writers.models import Writer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

# Create your views here.

@csrf_exempt
@api_view(['GET'])
def writers(request,format=None):
    writers = Writer.objects.all()
    serializer = Serializer(writers, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def writer(requset, pk,format=None):
    try:
        writer = Writer.objects.get(pk=pk)
    except Writer.DoesNotExist:
        return HttpResponse('Not found')

    if requset.method == 'GET':
        serializer = Serializer(writer)
        return Response(serializer.data)
    elif requset.method == 'PUT':
        data = JSONParser().parse(requset)
        serializer = SerializerWriter(Writer, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, safe=False)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif requset.method == 'DELETE':
        writer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['POST'])
def add(requset, format=None):
    if requset.method == 'POST':
        writer = Serializer(data=JSONParser().parse(requset))
        if writer.is_valid():
            writer.save()
            return Response(writer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(writer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

'''
curl -X PUT -F "name=AbdulRasol" -F "short=Google" -F "bio=From JSON" -F "image=D:\\MEGAsync\\tutorials\\django\\spimebook\\src\\Media\\author.jpg" -F "born_date=2023-10-05" 127.0.0.1:8000/writers/1/
'''