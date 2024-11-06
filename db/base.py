import asyncio
import os
from dotenv import load_dotenv

from ExFsParser import MovieScraper
from postgres import Postgres

load_dotenv('envs/dev.env')
db = Postgres(
    db_name=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=int(os.getenv('POSTGRES_PORT'))
)


async def init_db():
    # Connect to the database
    failed_connections: int = 0
    while failed_connections < 10:
        try:
            print("Connecting to db...")
            await db.connect()
            break
        except Exception as e:
            print("Connection faild. Retring")
            failed_connections += 1
            await asyncio.sleep(1)

    if failed_connections > 10:
        raise

    try:
        # Get the directory containing the current script
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        # Use os.path.join to create the correct path to init_db.sql
        sql_script_path = os.path.join(CURRENT_DIR, "init_db.sql")

        # Read the SQL script
        with open(sql_script_path, 'r') as file:
            sql_script = file.read()

        # Execute the initialization script
        await db.execute_transaction(sql_script)

    except Exception as e:

        raise e


async def create_movie(movie: MovieScraper):
    cond = f"movie_id = '{movie.get_id()}'"
    selected = await db.select_data('movies', 'movie_id', cond)

    if len(selected) > 0:
        await db.update_data('movies', {
                'type': movie.get_type(),
                'title': movie.get_title(),
                'poster': movie.get_poster(),
                'scenes': movie.get_scenes(),
                'rating': movie.get_rating(),
                'year_post': movie.get_year(),
                'country': movie.get_country(),
                'genrs': movie.get_genrs(),
                'duration': movie.get_duration(),
                'plot': movie.get_plot(),
                'certification': movie.get_certification(),
                'playlist': movie.get_playlist(),
            },
            cond
        )
    else:
        try:
            await db.insert_data('movies', {
                'movie_id': movie.get_id(),
                'type': movie.get_type(),
                'title': movie.get_title(),
                'poster': movie.get_poster(),
                'scenes': movie.get_scenes(),
                'rating': movie.get_rating(),
                'year_post': movie.get_year(),
                'country': movie.get_country(),
                'genrs': movie.get_genrs(),
                'duration': movie.get_duration(),
                'plot': movie.get_plot(),
                'certification': movie.get_certification(),
                'playlist': movie.get_playlist(),
            })
        except Exception as e:
            print(e)


