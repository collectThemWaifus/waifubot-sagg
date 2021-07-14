from backend import app
from flask_caching import Cache

config = {
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 120
}
app.config.from_mapping(config)
cache = Cache(app)
app.config['cache'] = cache
