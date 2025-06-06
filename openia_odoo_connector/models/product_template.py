# -*- coding: utf-8 -*-
import logging

import base64
import requests
from openai import OpenAI
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_create_image = fields.Boolean(string='Generate Image',
                                     help='Check this box if you want to automatically generate an image for this product')

    is_update_image = fields.Boolean(string='Update Image',
                                     help='Check this box if you want to automatically update an image for this product while changing the name.')

    @api.model
    def create(self, vals):
        """Generate image for the product upon creation if applicable."""
        res = super(ProductTemplate, self).create(vals)
        if not res.image_1920 and res.is_create_image:
            image_base64 = self.generate_image(res.name)
            if image_base64:
                res.write({'image_1920': image_base64})
            else:
                res.message_post(
                    body=(
                        f"Failed to generate image for product: '{res.name}' due to incorrect API key or other issues. "
                        f"Please verify your AI configuration and API key. You can get your API key at "
                        f"https://platform.openai.com/account/api-keys."
                    ),
                    message_type='notification'
                )
        return res

    def write(self, vals):
        """Update image if product name is changed and image update is enabled."""
        if 'name' in vals and 'image_1920' not in vals:
            is_update_image = vals.get('is_update_image', self.is_update_image)
            if is_update_image:
                image_base64 = self.generate_image(vals['name'])
                if image_base64:
                    vals['image_1920'] = image_base64
                else:
                    self.message_post(
                        body=(
                            f"Failed to update image for product: '{vals['name']}' due to incorrect API key or other issues. "
                            f"Please verify your AI configuration and API key. You can get your API key at "
                            f"https://platform.openai.com/account/api-keys."
                        ),
                        message_type='notification'
                    )
        return super(ProductTemplate, self).write(vals)

    def generate_image(self, name):
        """Function for generating images using AI based on the product name."""

        # Get the selected configuration ID from settings
        config_id = self.env['ir.config_parameter'].sudo().get_param('openia_odoo_connector.openia_id')
        if not config_id:
            return None

        config = self.env['openia'].sudo().search([('id', '=', int(config_id))], limit=1)
        if not config:
            return None

        # Create client with API key and base URL from the configuration
        client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )

        try:
            response = client.images.generate(
                model=config.image_model,
                prompt=name,
                size="1024x1024",
                n=1,
            )
            image_url = response.data[0].url
            response = requests.get(image_url)
            image_base64 = base64.b64encode(response.content)
        except Exception as e:
            _logger.error(f"Image generation failed: {str(e)}")
            return None

        return image_base64
