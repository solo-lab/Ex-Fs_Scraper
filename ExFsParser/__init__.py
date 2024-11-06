
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from .MoviesUrlScraper import MoviesUrlScraper
from .MovieScraper import MovieScraper

__all__ = ["MoviesUrlScraper", "MovieScraper", "logger"]