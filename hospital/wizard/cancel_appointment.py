from odoo import models, fields, api


class CancelAppointment(models.TransientModel):
    _name = 'hospital.cancel.appointment'
    _description = 'Cancel Appointment Wizard'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', readonly=True)
    reason = fields.Text(string='Reason')

    def app_cancel(self):
        self.appointment_id.state = 'cancel'
