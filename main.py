import logging
from logging.handlers import RotatingFileHandler
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from api_resource import APIResource
from configparser import ConfigParser
import helpers.utils as utils
from flask import Flask
from flask_restful import Api

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-conf", "--config_file", default="./config.properties", help="Location of the application config file")
parser.add_argument("-p", "--port", default=8080, type=int, help="Port")
parser.add_argument("-log", "--log_file", default=None, type=str, help="Location of the log file. Default is system log")
parser.add_argument("-logsize", "--log_max_size", default=1, type=int, help="Max file size in MB before it's rotated. Default is 1M. Set 0 to turn off log rotation")
parser.add_argument("-logcount", "--log_backup_count", default=5, type=int, help="Max number of rotated backup log file. Default is 5.")
parser.add_argument("-d", "--debug_level", default="WARNING", type=str, help="Debug Level CRITICAL/ERROR/WARNING/INFO/DEBUG. Default is WARNING")
args = vars(parser.parse_args())

PORT      = args["port"]
CONF_FILE = args["config_file"]
LOG_FILE  = args["log_file"]
LOG_LEVEL = args["debug_level"]
LOG_SIZE  = args["log_max_size"]
LOG_COUNT = args["log_backup_count"]

if __name__ == '__main__':
    try:
        if LOG_FILE is None:
            logging.basicConfig(filename=LOG_FILE, format='%(asctime)s %(levelname)s [%(name)s] %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level = LOG_LEVEL.upper())
        else:
            logging.basicConfig(handlers=[RotatingFileHandler(LOG_FILE, maxBytes=LOG_SIZE*1000000, backupCount=LOG_COUNT)], format='%(asctime)s %(levelname)s [%(name)s] %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level = LOG_LEVEL.upper())
        
        logger = logging.getLogger(__name__)

        #API Resources
        config_parser = ConfigParser()
        config_parser.read(CONF_FILE)
        config = utils.json_to_namespace(config_parser.get("SHELL_GATEWAY", "END_POINTS"))
        schema = config_parser.get("REQUEST_SCHEMA", "SCHEMA")

        #Setup API Server and end-points
        server = Flask("Shell Gateway")
        api = Api(server)
        for endpoint_config in config:
            api.add_resource(APIResource, endpoint_config.uri, resource_class_args=[[utils.json_namespace_to_str(endpoint_config), schema]], endpoint=endpoint_config.uri)

        server.run(debug = LOG_LEVEL.upper()==logging.getLevelName(logging.DEBUG), host = '0.0.0.0', port = PORT)

    except Exception as error:
        logger.fatal(f'Configuration setup failed! {error}')
    
    
