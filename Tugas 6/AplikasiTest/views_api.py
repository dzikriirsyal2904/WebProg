from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from AplikasiTest.models import Course
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def apiCourse(request):
    if request.method == "GET":
        # Serialize the data into json
        data = serializers.serialize("json", Course.objects.all())
        # Turn the JSON data into a dict and send as JSON response
        return JsonResponse(json.loads(data), safe=False)

    if request.method == "POST":
        # Turn the body into a dict
        body = json.loads(request.body.decode("utf-8"))
        # Check if the body is valid
        if not body or 'course_name' not in body:
            return HttpResponseBadRequest('Invalid data: Missing "course_name"')

        created = Course.objects.create(
            course_name=body['course_name']
        )
        return JsonResponse({"message": "data successfully created!"})

    if request.method == "PUT":
        # Turn the body into a dict
        body = json.loads(request.body.decode("utf-8"))
        # Check if the body is valid
        if not body or 'id' not in body or 'course_name' not in body:
            return HttpResponseBadRequest('Invalid data: Missing "id" or "course_name"')

        try:
            course = Course.objects.get(pk=body['id'])
            course.course_name = body['course_name']
            course.save()
            return JsonResponse({"message": "data successfully updated!"})
        except Course.DoesNotExist:
            return HttpResponseBadRequest('Course not found')

    if request.method == "DELETE":
        # Turn the body into a dict
        body = json.loads(request.body.decode("utf-8"))
        # Check if the body is valid
        if not body or 'id' not in body:
            return HttpResponseBadRequest('Invalid data: Missing "id"')

        try:
            course = Course.objects.get(pk=body['id'])
            course.delete()
            return JsonResponse({"message": "data successfully deleted!"})
        except Course.DoesNotExist:
            return HttpResponseBadRequest('Course not found')

    # Handle unsupported HTTP methods
    return HttpResponseBadRequest('Unsupported HTTP method')