'version API'

from flask import jsonify
from flask import current_app

def get_version():
    try:
        version_number = current_app.config['VERSION']
        current_app.logger.info('version: {}'.format(version_number))
        return jsonify({ 'version': version_number })
    except Exception as error:
        current_app.logger.error(
            'something went wrong while getting version: {}', error)
        return jsonify({'message': str(error)})