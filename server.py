import logging
import os.path

from waitress import serve

from app import app
from server_config import config

if not os.path.exists('log'):
    os.makedirs('log')
# setup logging save dir to ./log
logging.basicConfig(filename='log/server.log')
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.info('Server configuration:')
    logger.info(config)
    logger.info('Starting server...')
    serve(app, **config)
