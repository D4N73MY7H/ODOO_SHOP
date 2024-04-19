from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class Customer(models.Model):
    _name = 'all_tech.customer'
    _description = 'Customer'
    _rec_name = 'full_name'

    name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    email = fields.Char(string='E-Mail', required=True)
    phone = fields.Char(string='Phone', required=True)
    image = fields.Binary(string='Image', attachment=True)
    ref = fields.Char(string='Reference', readonly=True)

    _sql_constraints = [
        ('phone', 'unique (phone)', 'The phone must be unique!'),
        ('email', 'unique (email)', 'The email must be unique!'),
    ]

    @api.depends('name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            if record.name and record.last_name:
                record.full_name = f"{record.name} {record.last_name}"
            else:
                record.full_name = record.name or record.last_name

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if len(record.phone) != 11:
                raise ValidationError("Phone number must be less than 11")

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email:
                if not re.fullmatch(regex, self.email):
                    raise ValidationError("Invalid email format")

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('tech.customer.seq')
        return super(Customer, self).create(vals)

    def send_unpaid_invoice_reminders(self):
        self.env.cr.execute('''SELECT DISTINCT(customer_id) FROM all_tech_invoice where type='sell' ''')
        all_customers = self.env.cr.fetchall()

        for c in all_customers:
            customer_object =self.browse(c[0])
            all_invoices = self.env['all_tech.invoice'].search(
                [('customer_id', '=', c[0]), ('state', 'in', ['draft', 'paying'])])
            invoice_data_list = []
            counter = 0
            for invoice in all_invoices:
                invoice_data = {
                    'name': invoice.customer_id.full_name,
                    'date': invoice.date,
                    'invoice_number': invoice.invoice_num,
                    'invoice_total': round(invoice.total, 3),
                    'due_date': invoice.due_date,
                }
                invoice_data_list.append(invoice_data)
            template = self.env.ref('all_tech.email_template_unpaid_invoices')
            template.with_context({'invoices': invoice_data_list}).send_mail(customer_object.id)
























        # print(self)
        # invoices = self.env['all_tech.invoice'].read_group([
        #     ('type', '=', 'sell'),
        #     ('state', 'in', ['paying', 'draft'])
        # ], ['id'], ['customer_id'])
        #
        # for invoice in invoices:
        #     customer_id  =invoice['customer_id'][0]
        #     all_invoices = self.env['all_tech.invoice'].search([('customer_id', '=', customer_id),('state', '=', 'paid')])
        #     print(all_invoices)
        #     # for record in all_invoices:
        #     template = self.env.ref('all_tech.email_template_unpaid_invoices')
        #     template.with_context({'invoices': all_invoices}).send_mail(self.search([], limit=1).id)

        # for invoice in invoices:
        #     print(invoice)


        # invoices_list = [
        #     {
        #         'customer': invoice['customer_id'],
        #         'total': invoice['total'],
        #     } for invoice in invoices]
        #
        # template = self.env.ref('all_tech.email_template_unpaid_invoices')
        # template.with_context({'invoices': invoices_list}).send_mail(self.search([], limit=1).id)

