from odoo import models, fields, api


class Status(models.Model):
    _name = 'all_tech.status'
    _description = 'Invoice Status'
    _rec_name = 'status'

    status = fields.Char(string='Status', required=True)
    description = fields.Char(string='Description', required=True)
