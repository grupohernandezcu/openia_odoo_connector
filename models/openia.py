# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, _

class Openia(models.Model):
    _name = 'openia'
    _description = 'Openia'

    name = fields.Char('Name', required=True)
    base_url = fields.Char(string=_('Base url'), required=True, copy=False)
    api_key = fields.Char(
    string='API Key',
    required=True,
    copy=False)

    general_message_prompt = fields.Text(string=_('General message prompt'),help="This is the system prompt that will be used in the messages generated as a tool.")
    message_model = fields.Char(string=_('Message Model'), help="Model for getting response based on the message.", required=True)
    conversation_message_prompt = fields.Text(string=_('Conversation message prompt'),help="This is the system prompt that will be used in the messages in conversation.")
    conversation_model = fields.Char(string=_('Conversation Model'), help="This is the model that will be used in the conversations.", required=True)
    editing_model = fields.Char(string=_('Editing Model'), help="Model for editing (shortening, lengthening, and rephrasing) the description", required=True)
    converting_model = fields.Char(string=_('Converting Model'), help="Model for converting the audio from the file into text using AI. It returns the text.", required=True)
    image_model = fields.Char(string=_('Image Model'), help="Model for generating images for the product", required=True)

    temperature = fields.Float(string=_('Temperature'), required=True, default=0.5, help="Controls randomness: lower is more deterministic.")
    top_p = fields.Float(string=_('Top P'), default=1.0, help="Controls diversity via nucleus sampling.")
    frequency_penalty = fields.Float(string=_('Frequency Penalty'), default=0.0, help="How much to penalize new tokens based on their existing frequency.")
    presence_penalty = fields.Float(string=_('Presence Penalty'), default=0.0, help="How much to penalize new tokens based on whether they appear in the text so far.")
    max_tokens = fields.Integer(string=_('Max Tokens'), default=1024, help="Maximum number of tokens in the output.")
    stop_sequences = fields.Char(string=_('Stop Sequences'), help="Comma-separated list of stop sequences that will truncate the output.")