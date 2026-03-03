from django.shortcuts import render


# Mock Album class (temporary until we use real Django models)
class Album:
    def __init__(self, title, artist, year, rating, notes):
        self.title = title
        self.artist = artist
        self.year = year
        self.rating = rating
        self.notes = notes


# Mock data (simulating a database)
albums = [
    Album('Graduation', 'Kanye West', 2007, 9, 'Big, bright, confident production.'),
    Album('Discovery', 'Daft Punk', 2001, 10, 'A flawless electronic classic.'),
    Album('Currents', 'Tame Impala', 2015, 8, 'Synth-heavy and emotional.'),
    Album('Blonde', 'Frank Ocean', 2016, 10, 'Deeply personal and timeless.')
]


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def album_index(request):
    return render(request, 'albums/index.html', {
        'albums': albums
    })