# -*- coding: utf-8 -*-
from os import remove
from openai import OpenAI
from odoo import api, models

class ChatOdoo(models.Model):
    _name = 'open.chat'

    @api.model
    def get_response(self, message):
        # Get the selected configuration ID from settings
        config_id = self.env['ir.config_parameter'].sudo().get_param('openia_odoo_connector.openia_id')
        if not config_id:
            return "Error: No OpenAI model configured."

        config = self.env['openia'].sudo().search([('id', '=', int(config_id))], limit=1)
        if not config:
            return "Error: Configuration not found."

        # Prepare parameters for the API call
        params = {
            "model": config.message_model,
            "messages": [
                        {"role": "system", "content": config.general_message_prompt or ''},
                        {"role": "user", "content": message}
            ],
            "temperature": config.temperature,
            "top_p": config.top_p,
            "frequency_penalty": config.frequency_penalty,
            "presence_penalty": config.presence_penalty,
            "max_tokens": config.max_tokens,
        }

        # Add stop sequences if provided
        if config.stop_sequences:
            params["stop"] = [seq.strip() for seq in config.stop_sequences.split(",")]

        # Create client with API key and base URL from the configuration
        client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )

        try:
            chat_completion = client.chat.completions.create(**params)
        except Exception as e:
            error_text = str(e)
            # Handle error gracefully
            return f"Error: {error_text}"

        return chat_completion.choices[0].message.content


    @api.model
    def edit_content(self, message, message_type):
        """Function for editing (shortening, lengthening, and rephrasing) the content."""

        # Get the selected configuration ID from settings
        config_id = self.env['ir.config_parameter'].sudo().get_param('openia_odoo_connector.openia_id')
        if not config_id:
            return "Error: No OpenAI model configured."

        config = self.env['openia'].sudo().search([('id', '=', int(config_id))], limit=1)
        if not config:
            return "Error: Configuration not found."

        # Combine instruction type with the message
        prompt = f"{message_type}: {message}"

        # Prepare parameters for the API call
        params = {
            "model": config.editing_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": config.temperature,
            "top_p": config.top_p,
            "frequency_penalty": config.frequency_penalty,
            "presence_penalty": config.presence_penalty,
            "max_tokens": config.max_tokens,
        }

        # Add stop sequences if provided
        if config.stop_sequences:
            params["stop"] = [seq.strip() for seq in config.stop_sequences.split(",")]

        # Create client with API key and base URL from the configuration
        client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )

        try:
            chat_completion = client.chat.completions.create(**params)
        except Exception as e:
            error_text = str(e)
            return f"Error: {error_text}"

        return chat_completion.choices[0].message.content


    @api.model
    def convert_to_text(self, audio_path):
        """Function for converting audio to text using the configured AI model."""
        
        # Get the selected configuration ID from settings
        config_id = self.env['ir.config_parameter'].sudo().get_param('openia_odoo_connector.openia_id')
        if not config_id:
            return "Error: No OpenAI model configured."

        config = self.env['openia'].sudo().search([('id', '=', int(config_id))], limit=1)
        if not config:
            return "Error: Configuration not found."

        # Create client with API key and base URL from configuration
        client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )

        try:
            with open(audio_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model=config.converting_model,
                    file=audio_file
                )
            remove(audio_path)
        except Exception as e:
            return f"Error: {str(e)}"

        return transcription.text
