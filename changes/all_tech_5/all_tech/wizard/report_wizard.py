from odoo import models, fields, api
import base64
from collections import defaultdict
from ..reports import generate_report as gr

STATE_VALUES = {'draft': 'Draft',
                'paying': 'In Payment',
                'paid': 'Paid',
                'cancel': 'Cancelled'}


class PrintRaport(models.TransientModel):
    _name = 'all_tech.employee.report'
    _description = 'Employee Report Invoices'

    employee_id = fields.Many2one('all_tech.employee', string='Employee', readonly=True)
    date = fields.Date('Start Date')
    till = fields.Date('End Date')

    def print_report(self):
        info = {}
        extra = {}

        remaining_total_sum = 0
        total_sum = 0
        state_counts = defaultdict(int)
        counter = 0
        for rec in self:
            all_invoices = self.env['all_tech.invoice'].search([('user_id', '=', rec.employee_id.related_user.id),
                                                                ('date', '>=', rec.date),
                                                                ('date', '<=', rec.till)])
            all_invoices_data = []
            extras = []
            for i in all_invoices:
                counter += 1
                date_str = i.date.strftime('%d-%m-%y')
                num = i.invoice_num.split('-')[-1]
                all_invoices_data.append([num, date_str, i.customer_id.full_name, round(i.remaining_total, 3), round(i.total, 3), STATE_VALUES.get(i.state)])
                remaining_total_sum += i.remaining_total
                total_sum += i.total
                state_counts[i.state] += 1

            info['name'] = rec.employee_id.full_name
            info['id'] = rec.employee_id.id
            info['date'] = rec.date
            info['till'] = rec.till
            info['invoices'] = all_invoices_data
            extras.append([counter, state_counts.get('draft', 0), state_counts.get('paying', 0),
                           state_counts.get('paid', 0), state_counts.get('cancel', 0),
                           round(remaining_total_sum, 3), round(total_sum, 3)
                           ])
            extra['extras'] = extras

            pdf_data = gr.generate_pdf(info, extra)
            pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

            attachment = self.env['ir.attachment'].create({
                'name': 'report_{}.pdf'.format(rec.employee_id.full_name),
                'type': 'binary',
                'datas': pdf_base64,
                'res_model': self._name,
                'res_id': rec.id
            })
            return {
                'type': 'ir.actions.act_url',
                'url': 'web/content/?model=ir.attachment&id={}&field=datas&download=true&filename={}'.format(
                    attachment.id, attachment.name),
                'target': 'new',
            }
