# -*- coding: utf-8 -*-

from odoo import http
from pathlib import Path
from odoo.http import request
import os
from odoo.tools import json


class SpeechToText(http.Controller):
    @http.route('/upload_audio', type='http', auth='public', methods=['POST'], csrf=False)
    def upload_audio(self, **kwargs):
        """
            Function for uploading audio file into a file and
            returns the path of the file as json format
        """
        upload_dir = Path(__file__).parent
        file = kwargs.get('file')
        if file:
            file_path = os.path.join(upload_dir, file.filename)
            with open(file_path, 'wb') as f:
                f.write(file.read())
            return request.make_response(json.dumps({'filePath': file_path}), headers={'Content-Type': 'application/json'})
        return request.make_response(json.dumps({'error': 'No file uploaded'}), headers={'Content-Type': 'application/json'})


class OpeniaController(http.Controller):
    @http.route(['/openia_form'], type='http', auth="public", csrf=False,
                website=True)
    def question_submit(self):
        return http.request.render('openia_odoo_connector.connector')
