import subprocess
import logging
from flask import request
from flask_restful import Resource
import helpers.utils as utils
from jsonschema import validate, FormatChecker

class APIResource(Resource):
    ''' Resource class with API KEY Authentication supported
    '''

    __name__ = 'APIResource'
    _config = None
    _logger = logging.getLogger(__name__)
    _json_schema = {}

    def __init__(self, *args) -> None:
        super().__init__()
        self._config = utils.json_to_namespace(args[0][0])
        self._json_schema = utils.json_to_object(args[0][1])


    def get(self):
        return self.process_request(self.process_get)
    

    def post(self):
        return self.process_request(self.process_post)
    
    
    def put(self):
        return self.process_request(self.process_put)
    
    
    def process_request(self, callback):
        api_key = self.get_header_apikey()

        if api_key is not None and api_key == self.get_config_apikey():
            try:
                pay_load = self.process_payload()
                json_pay_load = utils.json_namespace_to_object(pay_load)
                validate(instance=json_pay_load, schema=self._json_schema, format_checker=FormatChecker())
                return callback()
            except Exception as error:
                self._logger.error (f'Receive invalid request with error: {error}')
                return self.process_invalid_schema()

        return self.process_invalid_apikey()


    def process_post(self):
        payload = self.process_payload()
        command = [self._config.target] + payload.args
        
        result = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return {'status': 200, 'data': result.stdout}, 200


    def process_get(self):
        return {'status': 501, 'message': 'Method not supported'}, 501


    def process_put(self):
        return {'status': 501, 'message': 'Method not supported'}, 501


    def process_payload(self):
        return utils.json_to_namespace(request.get_data(as_text=True))
    

    def process_invalid_schema(self):
        return {'status': 400, 'message': 'Invalid request data'}, 400
    

    def process_invalid_apikey(self):
        return {'status': 401, 'message': 'Authorization failed'}, 401
    

    def get_config_apikey(self):
        if self._config.api_key.key:
            return utils.base64_decode(self._config.api_key.key)
        else:
            return ""
    

    def get_header_apikey(self):
        api_key = ""
        if self._config.api_key.header and self._config.api_key.header in request.headers:
            api_key = request.headers[self._config.api_key.header]

        return api_key