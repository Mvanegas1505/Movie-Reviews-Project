from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64


from .models import Movie 
# Create your views here.
def home (request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html', {'name': 'Martin Vanegas Ospina'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
     movies = Movie.objects.filter(title__icontains=searchTerm)  #icontains for case-insensitive search
    else:
     movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})


def about (request):
    # return HttpResponse('<h1>HOLAAA!!!!</h1>')
    return render(request, 'about.html')



def statistics_view(request):
    matplotlib.use('Agg')
    
    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # -------- Gráfico de cantidad de películas por año --------
    movie_counts_by_year = {}

    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.figure(figsize=(8, 4))  
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png).decode('utf-8')

    # -------- Gráfico de cantidad de películas por género --------
    movie_counts_by_genre = {}

    for movie in all_movies:
        genre = movie.genre.split(',')[0] if movie.genre else "Unknown"  # Tomar solo el primer género
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1

    plt.figure(figsize=(8, 4))  
    plt.bar(movie_counts_by_genre.keys(), movie_counts_by_genre.values(), color='orange')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(rotation=45, ha='right')
   


    # Ajusta los márgenes para evitar que los nombres se corten
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})
    
