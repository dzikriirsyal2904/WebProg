from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from AplikasiTest.models import Course
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json, requests


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

@csrf_exempt
def consumeApiGet(request):
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    data = response.json()
    return render(request, "api-get.html", {'data': data})

@csrf_exempt
def consumeApiPost(request):
    if request.method == 'POST':
        try:
            data = {
                'title': 'foo',
                'body': 'bar',
                'userId': 1
            }
            response = requests.post("https://jsonplaceholder.typicode.com/posts", json=data)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            result = response.json()
            return render(request, "api-post.html", {'result': result})
        except requests.RequestException as e:
            return render(request, "error.html", {'error_message': str(e)})
    elif request.method == 'PUT':
        try:
            body = json.loads(request.body.decode("utf-8"))
            if not body:
                return JsonResponse({'message': 'data is not json type!'}, safe=False)

            api_url = body.get('api_url')
            update_data = body.get('update_data')
            if api_url and update_data:
                response = requests.put(api_url, json=update_data)
                if response.status_code == 200:
                    data = response.json()
                    return JsonResponse(data, safe=False)
                else:
                    return JsonResponse({'message': 'failed to update data at the API!'}, safe=False)
            else:
                return JsonResponse({'message': 'invalid request data!'}, safe=False)
        except json.JSONDecodeError as e:
            return JsonResponse({'message': str(e)}, safe=False)
        except requests.RequestException as e:
            return JsonResponse({'message': str(e)}, safe=False)
    else:
        return render(request, "api-post.html")