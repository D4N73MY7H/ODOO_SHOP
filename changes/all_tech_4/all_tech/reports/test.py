from datetime import datetime
import psycopg2
from odoo import models

dict_format = {
    'koka': {'bold': True, 'border': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Calibri', 'font_size': 14, 'bg_color': '#ededed', 'color': 'black'},
    'koka2': {'bold': True, 'border': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Calibri', 'font_size': 12, 'bg_color': '#ededed', 'color': 'black'},
    'header': {'bold': False, 'border': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Calibri', 'font_size': 11, 'bg_color': 'white', 'color': 'black'},
    'header_totale': {'bold': True, 'border': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Calibri', 'font_size': 14, 'bg_color': 'white', 'color': 'black'},
    'data_ora': {'bold': False, 'border': True, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Calibri', 'font_size': 12, 'bg_color': 'white', 'color': 'black'},
    'header_second': {'bold': True, 'border': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Calibri', 'font_size': 11, 'bg_color': 'white', 'color': 'black'},
    'koka_lart': {'bold': False, 'border': True, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Calibri', 'font_size': 12, 'bg_color': 'white', 'color': 'black'},
    'document_price': {'border': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'SansSerif', 'font_size': 11, 'color': 'black'},
    'vertical': {'bold': True, 'border': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter', 'font_name': 'Calibri', 'font_size': 11, 'rotation': 90, 'bg_color': '#C0C0C0'},
    'totals': {'bold': False, 'border': True, 'align': 'center', 'valign': 'vcenter', 'font_name': 'Calibri', 'font_size': 14, 'bg_color': 'white', 'color': 'black'},
    'number': {'border': True, 'align': 'right', 'valign': 'vcenter', 'font_name': 'Calibri', 'font_size': 12, 'bg_color': 'white', 'color': 'black'},
}


class ReportTipiKontrates(models.AbstractModel):
    _name = 'report.impro_kpp.raport.statistikor.tipi.kontrates'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, assets):
        worksheet = workbook.add_worksheet('Raporte statistikore per Ankesat')
        worksheet.set_column('A:J', 20)
        row = 0
        worksheet.merge_range(row, 0, row, 9, 'Statusi i Ankesave sipas Tipit te Kontrates per vitin 2022',
                              workbook.add_format(dict_format.get('koka')))
        row += 1
        worksheet.merge_range(row, 0, row, 1, 'Tipi i Kontrates', workbook.add_format(dict_format.get('koka')))
        worksheet.merge_range(row, 2, row, 3, 'Pranuar', workbook.add_format(dict_format.get('koka')))
        worksheet.merge_range(row, 4, row, 5, 'Mospranuar', workbook.add_format(dict_format.get('koka')))
        worksheet.merge_range(row, 6, row, 7, 'Ceshtje te Mbyllura', workbook.add_format(dict_format.get('koka')))
        worksheet.merge_range(row, 8, row, 9, 'Terheqje nga Ankesa', workbook.add_format(dict_format.get('koka')))
        row += 1
        # ID a tipeve te kontratave nga tabela "contract_type":
        # Sherbime - 2
        # Mallra - 3
        # Pune - 4
        contract_types = [('Sherbime', 2), ('Mallra', 3), ('Pune', 4)]
        states = ['qualified', 'disqualified', 'closed_case', 'withdrawn', ]
        for contract_type, c_id in contract_types:
            column = 0
            worksheet.merge_range(row, column, row, column + 1, contract_type,
                                  workbook.add_format(dict_format.get('koka')))
            for state in states:
                column += 2
                self.env.cr.execute("""
                                    SELECT count(a.id)
                                    FROM appeals_appeals AS a
                                    INNER JOIN procedure_procedure AS p ON a.procedure_id = p.id
                                    WHERE p.contract_type_id = %s and a.state= %s;
                                    """, (c_id, state))
                result = self.env.cr.fetchall()
                worksheet.merge_range(row, column, row, column + 1, result[0][0],
                                      workbook.add_format(dict_format.get('koka')))
            row += 1
        worksheet.merge_range(row, 0, row, 1, "Total", workbook.add_format(dict_format.get('koka')))
        worksheet.merge_range(row, 2, row, 3, "=SUM(C3:D5)", workbook.add_format(dict_format.get('koka')))
        worksheet.merge_range(row, 4, row, 5, "=SUM(E3:F5)", workbook.add_format(dict_format.get('koka')))
        worksheet.merge_range(row, 6, row, 7, "=SUM(G3:H5)", workbook.add_format(dict_format.get('koka')))
        worksheet.merge_range(row, 8, row, 9, "=SUM(I3:J5)", workbook.add_format(dict_format.get('koka')))