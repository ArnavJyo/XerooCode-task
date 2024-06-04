
from django.http import JsonResponse
from .models import ClusterDetails
from github_connect.models import Repository 

def cluster_data(request):
    clusters = ClusterDetails.objects.values()
    return JsonResponse(list(clusters), safe=False)
