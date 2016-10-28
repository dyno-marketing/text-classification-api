import sys
from config import config
from app import app, setup_logging
import logging

if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    debug = False
    dev_mode = 'dev'
    log_mode = 'log'

    if log_mode in str(sys.argv):
        setup_logging()

    if dev_mode in str(sys.argv):
        debug = True

    logger = logging.getLogger(__name__)

    logger.info("start rd_report_api")

    app.run(debug=debug, host=config.BACKEND_CONFIG['server'], port=config.BACKEND_CONFIG['port'])

    logger.error("stop rd_report_api")
