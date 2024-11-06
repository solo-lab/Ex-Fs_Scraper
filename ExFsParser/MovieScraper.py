import uuid
from typing import List, Any, Optional
from . import logger
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Movie(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    poster: Optional[str] = None
    scenes: Optional[List[str]] = None
    rating: Optional[float] = None
    year: Optional[int] = None
    country: Optional[List[str]] = None
    genrs: Optional[List[str]] = None
    duration: Optional[str] = None
    plot: Optional[str] = None
    certification: Optional[str] = None
    playlist: Optional[List[str]] = None


class MovieScraper:
    def __init__(self, movie_url: str):
        self._movie = self._parse_site(movie_url)

    def get_id(self):
        return self._movie.id if self._movie else "No movie data"

    def get_type(self):
        return self._movie.type if self._movie else "No movie data"

    def get_title(self):
        return self._movie.title if self._movie else "No movie data"

    def get_poster(self):
        return self._movie.poster if self._movie else "No movie data"

    def get_scenes(self):
        return self._movie.scenes if self._movie else "No movie data"

    def get_rating(self):
        return self._movie.rating if self._movie else "No movie data"

    def get_year(self):
        return self._movie.year if self._movie else "No movie data"

    def get_country(self):
        return self._movie.country if self._movie else "No movie data"

    def get_genrs(self):
        return self._movie.genrs if self._movie else "No movie data"

    def get_duration(self):
        return self._movie.duration if self._movie else "No movie data"

    def get_plot(self):
        return self._movie.plot if self._movie else "No movie data"

    def get_certification(self):
        return self._movie.certification if self._movie else "No movie data"

    def get_playlist(self):
        return self._movie.playlist if self._movie else "No movie data"

    def _parse_site(self, movie_url: str) -> Movie:
        try:
            response = requests.get(movie_url)
            response.encoding = 'utf-8'
        except Exception as e:
            logger.error(f"Error fetching site: {e}")
            return Movie()

        site_html = response.text
        soup = BeautifulSoup(site_html, features="html.parser")

        eror_film = soup.find('div', {'class': 'clr Info'})
        if eror_film:
            raise Exception('Заблочен')

        id_film = movie_url.split('/')[-1].split('.')[0]

        type_movie = movie_url.split('/')[-2]
        name_film = soup.select_one('h1.view-caption')
        name_film = name_film.text.strip().replace('смотреть онлайн', '').strip() if name_film else "Unknown Title"

        poster_film = soup.find('div', {'class': 'FullstoryFormLeft'})
        poster_url = poster_film.find('img')['src'] if poster_film and poster_film.find('img') else None

        scenes_film = soup.find_all('a', {'class': 'lightbox'})
        scenes = []
        for elemant in scenes_film:
            scenes.append(elemant['href'])

        rating_film = soup.find('div', {'class': 'in_name_imdb'}).text


        year_film = int(soup.find('p', {'class': 'FullstoryInfoin'}).text)

        country_elements = soup.select('p.FullstoryInfoin a[href*="/country/"]')
        countries = [element.get_text() for element in country_elements]

        genre_list = soup.select('p.FullstoryInfoin a[href*="/genre/"]')
        genres = [element.get_text() for element in genre_list]

        duration_film = soup.select_one('p.FullstoryInfoin:-soup-contains("мин.")').text.strip()

        plot_film = soup.find('div', {'class': 'FullstorySubFormText'}).text

        sertification_tag = soup.find('p', {'class': 'FullstoryInfoAge infoi_age'})
        sertification = sertification_tag.text if sertification_tag else None

        playlist_film = soup.find('div', {'class': 'tab-content'})
        film = playlist_film.find_all('div', {'class': 'tab-pane'})
        films_array = []
        for pane in film:
            iframe = pane.find('iframe')
            if iframe:
                films_array.append(iframe['src'])

        # print(films_array)

        return Movie(
            id= id_film,
            type= type_movie,  # TODO: Extract from URL
            title=name_film,
            poster=poster_url,
            scenes=scenes,
            rating=float(rating_film) if rating_film else None,
            year= year_film,  # TODO: Extract from URL
            country=countries,
            genrs=genres,
            duration=duration_film,
            plot=plot_film,
            certification=sertification,
            playlist=films_array
        )
