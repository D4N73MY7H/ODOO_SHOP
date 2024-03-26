from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Invoice(models.Model):
    _name = 'all_tech.invoice'
    _description = 'Invoice'
    _rec_name = 'invoice_num'

    invoice_num = fields.Char(readonly=True)
    date = fields.Datetime(string='Date', required=True, default=lambda self: fields.Datetime.now())
    sale_items_ids = fields.One2many('all_tech.sale_item', 'invoice_id', string='Sale Items', required=True)
    type = fields.Selection([('buy', 'Buy'), ('sell', 'Sell')], required=True, string='Type')
    employee_id = fields.Many2one('all_tech.employee', string='Employee')
    supplier_id = fields.Many2one('all_tech.supplier', string='Supplier')
    customer_id = fields.Many2one('all_tech.customer', string='Customer')
    total = fields.Float(string='Total', compute='_compute_total_price', store=True)

    _sql_constraints = [
        ('invoice_num', 'unique (invoice_num)', 'The invoice number must be unique!'),
    ]

    @api.constrains('sale_items_ids')
    def _check_sale_items(self):
        for invoice in self:
            if not invoice.sale_items_ids:
                raise ValidationError('An invoice must have at least one sale item.')

    @api.constrains('invoice_num')
    def _check_unique_invoice_num(self):
        for record in self:
            if record.invoice_num:
                existing_invoice = self.env['all_tech.invoice'].search(
                    [('invoice_num', '=', record.invoice_num), ('id', '!=', record.id)])
                if existing_invoice:
                    raise ValidationError("The invoice number must be unique!")

    @api.model
    def create(self, vals):
        vals['invoice_num'] = self.env['ir.sequence'].next_by_code('all_tech.invoice.sequence')
        return super(Invoice, self).create(vals)

    @api.depends('sale_items_ids.total_price')
    def _compute_total_price(self):
        for rec in self:
            rec.total = sum(rec.sale_items_ids.mapped('total_price'))

    def buy(self):
        if self.type == 'buy':
            for sale_item in self.sale_items_ids:
                sale_item.product_id.quantity += sale_item.quantity
        else:
            for sale_item in self.sale_items_ids:
                sale_item.product_id.quantity -= sale_item.quantity
                sale_item.product_id.price = sale_item.price


class SaleItem(models.Model):
    _name = 'all_tech.sale_item'
    _description = 'Sale Items'

    price = fields.Float(string='Price', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    product_id = fields.Many2one('all_tech.product', string='Product', required=True)
    invoice_id = fields.Many2one('all_tech.invoice', string='Invoice', required=True)
    sale_date = fields.Datetime(string='Date', required=True, default=lambda self: fields.Datetime.now())
    total_price = fields.Float(string='Total', compute='_compute_total_price', store=True)

    @api.depends('quantity', 'price')
    def _compute_total_price(self):
        for sale_item in self:
            sale_item.total_price = sale_item.quantity * sale_item.price

    @api.onchange('product_id', 'invoice_id')
    def onchange_product_id(self):
        if self.product_id and self.invoice_id:
            if self.invoice_id.type == 'buy':
                self.price = self.product_id.price
            else:
                self.price = self.product_id.unit_price
