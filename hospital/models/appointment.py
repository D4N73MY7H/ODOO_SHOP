from odoo import models, fields, api
import random


def generate_app_ref():
    ref = [str(random.randint(0, 9)) for _ in range(5)]
    return ''.join(ref)


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ref'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    gender = fields.Selection(related='patient_id.gender')
    time = fields.Datetime(string='Time', required=True, default=fields.Datetime.now)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    ref = fields.Char(string='Reference', readonly=True)
    doctor_id = fields.Many2one('res.users', string='Doctor')
    prescription = fields.Html(string='Prescription')
    pharmacy_lines_ids = fields.One2many('hospital.pharmacy.lines',  'app_id', string='Pharmacy Lines')
    priority = fields.Selection([
        ('0', 'Very Low'),
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High'),
        ('4', 'High'),
        ('5', 'Maximal')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('inConsultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='draft',string="Status", required=True, tracking=True)

    # @api.onchange('ref', 'patient_id')
    # def _onchange_ref(self):
    #     a = generate_app_ref()
    #     if self.patient_id:
    #         self.ref = f"APP{a}{self.patient_id.id}"

    def app_draft(self):
        self.state = 'draft'

    def app_done(self):
        self.state = 'done'

    def app_consultation(self):
        self.state = 'inConsultation'

    def app_cancel(self):
        action = self.env.ref('hospital.hospital_cancel_appointment').read()[0]
        self.state = 'cancel'
        return action

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].sudo().next_by_code('hospital.appointment.sequence')
        print(sequence)
        vals['ref'] = sequence
        appointment = super(Appointment, self).create(vals)
        self.env.cr.commit()  # Explicitly commit the transaction
        return appointment

    # @api.model
    # def create(self, vals):
    #     print(self.env['ir.sequence'].next_by_code('hospital.appointment.sequence'))
    #     vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence')
    #     return super(Appointment, self).create(vals)

    def print_id(self):
        print(self.patient_id.id)

    # @api.constrains('patient_id')
    # def onchange_patient_id(self):
    #     if self.patient_id:
    #         year = self.patient_id.date_of_birth.year if self.patient_id.date_of_birth else 'Unknown'
    #         self.ref = f"REF{self.patient_id.id}{year}"
    #
    # @api.onchange('ref', 'patient_id')
    # def onchange_patient_id(self):
    #     if self.patient_id:
    #         year = self.patient_id.date_of_birth.year if self.patient_id.date_of_birth else 'Unknown'
    #         self.ref = f"REF{self.patient_id.id}{year}"


class PharmacyLines(models.Model):
    _name = 'hospital.pharmacy.lines'
    _description = 'Pharmacy Lines'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    price = fields.Float(related='product_id.list_price', string="Price")
    quantity = fields.Integer(string="Quantity", required=True)
    app_id = fields.Many2one('hospital.appointment', string="Appointment")
