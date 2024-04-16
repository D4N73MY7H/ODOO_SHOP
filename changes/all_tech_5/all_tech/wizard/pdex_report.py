from odoo import api, fields, models


class PdexReport(models.TransientModel):
    _name = 'all_tech.pdex'
    _description = 'Pdex Report'

    date = fields.Date('Start Date')
    till = fields.Date('End Date')
    report_type = fields.Selection(string='Report Type', selection=[('pdf', 'PDF'), ('xls', 'XLS'), ],
                                   required=True)

    def print_pdex_report(self):
        data = {
            'date': self.date,
            'till': self.till,
        }
        if self.report_type == 'pdf':
            return self.env.ref('all_tech.action_pdex_report_pdf').report_action(None, data=data)
        else:
            return self.env.ref('all_tech.action_pdex_report_xls').report_action(None, data=data)
