from odoo import models, fields, api


class CancelAppointment(models.TransientModel):
    _name = 'hospital.cancel.appointment'
    _description = 'Cancel Appointment Wizard'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    reason = fields.Text(string='Reason')

    def app_cancel(self):
        return