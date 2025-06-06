# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError
from openai import OpenAI

class Channel(models.Model):
    _inherit = 'mail.channel'

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
        openia_channel = self.env.ref('openia_odoo_connector.channel_openia')
        user_openia = self.env.ref("openia_odoo_connector.user_openia")
        partner_openia = self.env.ref("openia_odoo_connector.partner_openia")
        author_id = msg_vals.get('author_id')
        prompt = msg_vals.get('body')
        if not prompt:
            return rdata

        if self.channel_type == 'chat':
            if author_id != partner_openia.id and (
                str(partner_openia.name or '') + ', ' in msg_vals.get('record_name', '') or
                'OpenIA,' in msg_vals.get('record_name', '')
            ):
                try:
                    res = self._get_openia_response(prompt=prompt)
                    self.with_user(user_openia).message_post(
                        body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
                except Exception as e:
                    raise UserError(_(str(e)))

        elif msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == openia_channel.id:
            if author_id != partner_openia.id:
                try:
                    res = self._get_openia_response(prompt=prompt)
                    openia_channel.with_user(user_openia).message_post(
                        body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
                except Exception as e:
                    raise UserError(_(str(e)))

        return rdata

    def _get_openia_response(self, prompt):
        
        # Get the selected configuration ID from settings
        config_id = self.env['ir.config_parameter'].sudo().get_param('openia_odoo_connector.openia_id')
        if not config_id:
            return "Error: No OpenAI model configured."

        config = self.env['openia'].sudo().search([('id', '=', int(config_id))], limit=1)
        if not config:
            return "Error: Configuration not found."
        
        client = OpenAI(api_key=config.api_key, base_url=config.base_url)

        # Construir mensajes con prompt general + prompt usuario
        messages = []
        if config.conversation_message_prompt:
            messages.append({"role": "system", "content": config.conversation_message_prompt})
        messages.append({"role": "user", "content": prompt})

        params = {
            "model": config.conversation_model,
            "messages": messages,
            "temperature": config.temperature or 0.5,
            "top_p": getattr(config, 'top_p', 1),
            "frequency_penalty": getattr(config, 'frequency_penalty', 0),
            "presence_penalty": getattr(config, 'presence_penalty', 0),
            "max_tokens": getattr(config, 'max_tokens', 1500),
            "user": self.env.user.name,
        }

        try:
            response = client.chat.completions.create(**params)
            return response.choices[0].message.content
        except Exception as e:
            raise UserError(_("OpenAI API error: %s") % str(e))