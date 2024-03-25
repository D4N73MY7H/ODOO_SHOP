from odoo import models, fields, api


class Type(models.Model):
    _name = 'all_tech.type'
    _description = 'Customer Type'
    _rec_name = 'type'

    type = fields.Char(string='Type', required=True)
    description = fields.Char(string='Description', required=True)