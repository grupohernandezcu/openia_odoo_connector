# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Add field to configuration settings"""
    _inherit = "res.config.settings"

    openia_id = fields.Many2one(
        comodel_name='openia',
        string="Model AI",
        config_parameter='openia_odoo_connector.openia_id',
        help="Select the model configuration you want to use"
    )