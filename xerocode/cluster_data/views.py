
from django.http import JsonResponse
from .models import ClusterDetails
from github_connect.models import Repository 

def cluster_data(request):
    # Retrieve authenticated user information passed from GitHub Connect app
    authenticated_user_id = request.session.get('authenticated_user')
    if authenticated_user_id:
        # Filter cluster details based on the authenticated user
        clusters = ClusterDetails.objects.filter(user_id=authenticated_user_id).values()
        return JsonResponse(list(clusters), safe=False)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)