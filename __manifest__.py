# -*- coding: utf-8 -*-
{
    "name": "OpenAI Odoo Connector",
    "version": "16.0.1.0.0",
    "category": "Productivity, Extra Tools ",
    "summary": "User can create content, Generate product image and Convert spoken language into written text using AI.",
    "description": """ This module simplifies content creation and editing by integrating with artificial intelligence models that work with the Openia API.
    It also facilitates the generation of images for newly created products and the modification of product names.
    Additionally, it includes a speech-to-text feature that allows users to convert spoken language into written text, enabling hands-free interaction and further streamlining the content creation process. It also allows users to chat with artificial intelligence from the conversations module.""",
    'author': 'Grupo Hernandez',
    'company': 'Grupo Hernandez',
    'maintainer': 'Grupo Hernandez',
    'website': "https://www.grupohernandez.cu",
    'depends': ['mail', 'product', 'web_editor'],
    "data": [
        "security/ir.model.access.csv",
        "views/openia_views.xml",
        "data/mail_channel_data.xml",
        "data/user_partner_data.xml",
        "data/openia_default_data.xml",
        "views/product_product.xml",
        "views/product_template.xml",
        "views/res_config_settings_views.xml"
    ],
    'assets': {
        'web_editor.assets_wysiwyg': [
            'openia_odoo_connector/static/src/xml/web_editor_toolbar.xml',
            'openia_odoo_connector/static/src/xml/alternative_chatgpt.xml',
        ],
        'web.assets_backend': [
            'openia_odoo_connector/static/src/css/chatgpt_odoo.css',
            'openia_odoo_connector/static/src/js/wysiwyg.js',
            'openia_odoo_connector/static/src/js/open_chatgpt.js',
            'openia_odoo_connector/static/src/js/recordAudio.js',
            'openia_odoo_connector/static/src/js/custom_toolbar.js',
            'openia_odoo_connector/static/src/js/alternative_chatgpt.js',
        ],
    },
    'external_dependencies': {'python': ['openai']},
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
