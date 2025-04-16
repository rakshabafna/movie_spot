from django.shortcuts import render
from django.conf import settings
import requests
from users.models import UserList

API_KEY = settings.TMDB_API_KEY

def landing_page(request):
    category = request.GET.get("category", "popular")
    search_query = request.GET.get("search", "")
    page = int(request.GET.get("page", 1))
    next_page = page + 1
    base_url = 'https://api.themoviedb.org/3/movie/'
    error_message = ""
    user_lists = UserList.objects.filter(user=request.user) if request.user.is_authenticated else None
    if search_query:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={search_query}&page={page}"
    else:
        url = f"{base_url}{category}?api_key={API_KEY}&page={page}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get('results', [])
        total_pages = response.json().get("total_pages", 1)
        has_next = page < total_pages
    except Exception as e:
        data = []
        error_message = "Something went wrong"
        has_next = False

    if request.headers.get("HX-Request"):
        return render(request, 'movies/partials/movie_list.html', {
            "movies": data,
            "category": category,
            "search_query": search_query,
            "error_message": error_message,
            "next_page": next_page,
            "has_next": has_next
        })

    return render(request, 'movies/landing.html', {
        "movies": data,
        "category": category,
        "search_query": search_query,
        "error_message": error_message,
        "next_page": next_page,
        "has_next": has_next
    })


def movie_detail(request, movie_id):
    movie_detail_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}'
    movie_credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    error_message = ""

    movie_data = None
    credits_data = []

    try:
        movie_detail_response = requests.get(movie_detail_url)
        movie_detail_response.raise_for_status()
        movie_data = movie_detail_response.json()
    except Exception as e:
        error_message = "Could not fetch movie details."
        movie_data = None  # Ensure it's defined

    try:
        movie_credits_response = requests.get(movie_credits_url)
        movie_credits_response.raise_for_status()
        credits_data = movie_credits_response.json()
    except Exception as e:
        error_message = "Could not fetch movie credits."
        credits_data = []  # Ensure it's defined

    if not movie_data:
        return render(request, "movies/movie_not_found.html", {"error_message": error_message})

    return render(request, "movies/movie_detail.html", {
        "movie": movie_data,
        "credits": credits_data,
        "error_message": error_message,
    })
