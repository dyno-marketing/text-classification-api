import sys
from config import config
from app import app, setup_logging
import logging

if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    debug = False

    if "enable_log_flag" in str(sys.argv):
        setup_logging()

    if "enable_debug_mode" in str(sys.argv):
        debug = True

    logger = logging.getLogger(__name__)

    logger.info("start api at ", )
    app.run(debug=debug, host=config.BACKEND_CONFIG['server'], port=config.BACKEND_CONFIG['port'])
    logger.error("stop api")
