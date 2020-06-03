import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from .models import Search

BASE_CRAIGLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# result = True
# final_postings = []


def home(request):
    return render(request, 'base.html')


def new_search(request):
    # global result
    # global final_postings

    search = request.POST.get('search')
    Search.objects.create(search=search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for postings in post_listings:
        post_title = postings.find(class_='result-title').text
        post_url = postings.find('a').get('href')
        if postings.find(class_='result-price'):
            post_price = postings.find(class_='result-price').text
        else:
            post_price = "NA"

        if postings.find(class_='result-image gallery'):
            image_id = postings.find(class_='result-image gallery').get('data-ids').split(',')
            url_image_id = image_id[0]
            post_image = BASE_IMAGE_URL.format(url_image_id[2:])
        else:
            post_image = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAA1BMVEX///+nxBvIAAAAR0lEQVR4nO3BAQ0AAADCoPdPbQ8HFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPBgxUwAAU+n3sIAAAAASUVORK5CYII='

        final_postings.append((post_title, post_url, post_price, post_image))

    data_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'craiglistscrapper/new_Search.html', data_for_frontend)