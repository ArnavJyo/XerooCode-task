from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest,HttpResponse
from .models import Repository
from requests.exceptions import RequestException
import requests
def hello_world(request):
  return HttpResponse('<h1>Xero code task </h1>')
def github_login(request):
  client_id = settings.GITHUB_CLIENT_ID
  redirect_uri = request.build_absolute_uri('/github/callback')
  return redirect(f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=repo')

def github_callback(request):
  code = request.GET.get('code')
  if not code:
      return HttpResponseBadRequest('Missing authorization code')

  client_id = settings.GITHUB_CLIENT_ID
  client_secret = settings.GITHUB_CLIENT_SECRET

  try:
      # Exchange code for access token
      token_response = requests.post('https://github.com/login/oauth/access_token', data={
          'client_id': client_id,
          'client_secret': client_secret,
          'code': code,
      }, headers={'Accept': 'application/json'}).json()

      access_token = token_response.get('access_token')
      if not access_token:
          return HttpResponseBadRequest('Failed to obtain access token')

      # Fetch user repositories
      repos_response = requests.get('https://api.github.com/user/repos', headers={
          'Authorization': f'token {access_token}'
      }).json()

      # Save repositories to the database (update only changed fields)
      for repo in repos_response:
          repo_data, created = Repository.objects.update_or_create(
              full_name=repo['full_name'],
              defaults={
                  'name': repo['name'],
                  'private': repo['private'],
                  'html_url': repo['html_url'],
                  'description': repo['description'],
                  'created_at': repo['created_at'],
                  'updated_at': repo['updated_at'],
              }
          )

      return JsonResponse({'status': 'Repositories fetched and stored successfully'})

  except RequestException as e:
      print(f"Error fetching repositories: {e}")
      return HttpResponseBadRequest('Failed to retrieve repositories')

def display_repository_details(request):
  repositories = Repository.objects.all()
  return render(request, 'github_details.html', {'repositories': repositories})
