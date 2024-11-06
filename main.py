import asyncio
import time

from db.base import init_db, create_movie
from ExFsParser import MoviesUrlScraper, MovieScraper


async def main():
    await init_db()

    start_time = time.time()

    movies_url_scraper = MoviesUrlScraper('serials')

    max_pages = movies_url_scraper.max_pages()
    #                     189
    for page in range(1, max_pages + 1):
        print(f"PAGEEEEEEEE {page}")
        if page % 3 == 0:
            await asyncio.sleep(60)
        for movie_url in movies_url_scraper.get_movie_urls(page):
            try:
                movie = MovieScraper(movie_url)
                print(movie.get_id())
                await create_movie(movie)
            except Exception as e:
                print(e)

    print(f"--- {(time.time() - start_time):.2f} seconds ---")

    # print(movie)


if __name__ == "__main__":
    asyncio.run(main())
