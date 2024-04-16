from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class Invoice(models.Model):
    _name = 'all_tech.invoice'
    _description = 'Invoice'
    _rec_name = 'invoice_num'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    invoice_num = fields.Char(readonly=True)
    date = fields.Date(string='Date', required=True, default=lambda self: fields.Date.context_today(self))
    due_date = fields.Date(string='Due', store=True)
    sale_items_ids = fields.One2many('all_tech.sale_item', 'invoice_id', string='Sale Items', required=True, tracking=True)
    payments_ids = fields.One2many('all_tech.payment', 'invoice_id', string='Payments', required=True, tracking=True)
    type = fields.Selection([('buy', 'Buy'), ('sell', 'Sell')], required=True, string='Type')
    employee_id = fields.Many2one('all_tech.employee', string='Employee')
    user_id = fields.Many2one(comodel_name='res.users', string='Employee', readonly=True,
                                  default=lambda self: self.env.user.id)
    supplier_id = fields.Many2one('all_tech.supplier', string='Supplier')
    customer_id = fields.Many2one('all_tech.customer', string='Customer')
    total = fields.Float(string='Total', compute='_compute_total_price', store=True)
    remaining_total = fields.Float(string='Remaining Total', compute='_compute_payment_amount', store=True)
    tax_rate = fields.Float(string='Tax Rate', default=10.0, help='Tax rate in percentage')
    active = fields.Boolean(string='Active', default=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('paying', 'In Payment'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled')], default='draft', string="Status", required=True, tracking=True)

    _sql_constraints = [
        ('invoice_num', 'unique (invoice_num)', 'The invoice number must be unique!'),
    ]

    @api.constrains('sale_items_ids')
    def _check_sale_items(self):
        for invoice in self:
            if not invoice.sale_items_ids:
                raise ValidationError('An invoice must have at least one sale item.')

    @api.onchange('date')
    def _compute_due_date(self):
        for record in self:
            if record.date:
                selected_date = fields.Date.from_string(record.date)
                record.due_date = selected_date + timedelta(days=30)

    # @api.constrains('invoice_num')
    # def _check_unique_invoice_num(self):
    #     for record in self:
    #         if record.invoice_num:
    #             existing_invoice = self.env['all_tech.invoice'].search(
    #                 [('invoice_num', '=', record.invoice_num), ('id', '!=', record.id)])
    #             if existing_invoice:
    #                 raise ValidationError("The invoice number must be unique!")

    # @api.onchange('date')
    # def _default_due_date(self):
    #     if self.date:
    #         selected_date = fields.Date.from_string(self.date)
    #         self.due_date = selected_date + timedelta(days=30)

    # @api.constrains('due_date')
    # def _check_due_date(self):
    #     for invoice in self:
    #         if invoice.due_date and invoice.due_date < fields.Datetime.now():
    #             raise ValidationError("Due date must be in the future.")

    @api.model
    def create(self, vals):
        vals['invoice_num'] = self.env['ir.sequence'].next_by_code('all_tech.invoice.sequence')
        return super(Invoice, self).create(vals)

    @api.depends('sale_items_ids.total_price', 'payments_ids.amount')
    def _compute_total_price(self):
        for rec in self:
            total_sales = sum(rec.sale_items_ids.mapped('total_price'))
            total_payments = sum(rec.payments_ids.mapped('amount'))
            rec.total = total_sales
            rec.remaining_total = total_sales - total_payments

    # @api.depends('total', 'remaining_total', 'due_date')
    # def _compute_total_amount_due(self):
    #     for invoice in self:
    #         if invoice.state != 'done' and invoice.due_date:
    #             # Calculate the number of months overdue
    #             due_date = fields.Datetime.from_string(invoice.due_date)
    #             current_date = fields.Datetime.now()
    #             months_overdue = (current_date.year - due_date.year) * 12 + current_date.month - due_date.month
    #             if months_overdue < 0:
    #                 months_overdue = 0
    #
    #             # Calculate tax based on overdue months
    #             tax_percentage = invoice.tax_rate / 100.0
    #             tax_amount = invoice.total * tax_percentage * months_overdue
    #
    #             # Update total amount due
    #             invoice.total_amount_due = invoice.total + tax_amount
    #
    # total_amount_due = fields.Float(string='Total Amount Due', compute='_compute_total_amount_due', store=True)

    @api.depends('payments_ids.amount')
    def _compute_payment_amount(self):
        for rec in self:
            total_payments = sum(rec.payments_ids.mapped('amount'))
            rec.remaining_total = rec.total - total_payments

    @api.onchange('remaining_total')
    def update_state(self):
        if not self.payments_ids:
            self.state = 'draft'
        elif self.remaining_total > 0:
            self.state = 'paying'
        elif self.remaining_total == 0:
            self.state = 'paid'

    def app_cancel(self):
        for item in self.sale_items_ids:
            item.product_id.quantity += item.quantity
        self.state = 'cancel'


class SaleItem(models.Model):
    _name = 'all_tech.sale_item'
    _description = 'Sale Items'

    price = fields.Float(string='Price')
    quantity = fields.Integer(string='Quantity', required=True)
    product_id = fields.Many2one('all_tech.product', string='Product', required=True)
    invoice_id = fields.Many2one('all_tech.invoice', string='Invoice', required=True)
    sale_date = fields.Datetime(string='Date', required=True, default=lambda self: fields.Datetime.now())
    discount = fields.Selection([('0', '0'), ('30%', '30%'), ('50%', '50%'), ('75%', '75%')], string='Discount', required=True, default='0')
    total_price = fields.Float(string='Total', compute='_compute_total_price', store=True)

    @api.depends('price', 'discount', 'quantity')
    def _compute_total_price(self):
        for sale_item in self:
            discount_factor = 1.0  # Initialize discount factor
            if sale_item.discount == '30%':
                discount_factor = 0.7  # 30% discount
            elif sale_item.discount == '50%':
                discount_factor = 0.5  # 50% discount
            elif sale_item.discount == '75%':
                discount_factor = 0.25  # 75% discount

            sale_item.total_price = sale_item.quantity * sale_item.price * discount_factor

    @api.onchange('product_id', 'invoice_id')
    def onchange_product_id(self):
        if self.product_id and self.invoice_id:
            if self.invoice_id.type == 'buy':
                self.price = self.product_id.price
            else:
                self.price = self.product_id.unit_price

    @api.model
    def create(self, vals):
        record = super(SaleItem, self).create(vals)

        if record.invoice_id.type == 'buy':
            record.product_id.quantity += record.quantity
            record.product_id.price = record.price
        else:
            record.product_id.quantity -= record.quantity
            if record.product_id.quantity < record.quantity:
                raise ValidationError('The quantity of the product is not enough.')

        return record


class Payments(models.Model):
    _name = 'all_tech.payment'
    _description = "Payments completed"

    amount = fields.Float(string='Amount', required=True)
    date = fields.Datetime(string='Date', required=True, default=lambda self: fields.Datetime.now())
    invoice_id = fields.Many2one('all_tech.invoice', string='Invoice', required=True)

    @api.constrains('amount')
    def _check_amount_not_empty(self):
        for payment in self:
            if payment.amount <= 0:
                raise ValidationError("Amount cannot be 0.")
