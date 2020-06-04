from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@require_http_methods(["GET"])
@csrf_exempt
def create_user(request):
    
    return JsonResponse({"status": True})