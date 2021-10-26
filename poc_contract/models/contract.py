# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    structured_comm = fields.Char(string="Structured communication", required=True)
    payment_mode = fields.Selection([
        ('transfer', 'Wire transfer'),
        ('mandate', 'Mandate')],
        required=True
    )
    recurring_rule_type = fields.Selection(
        [
            ("monthly", "Month(s)"),
            ("quarterly", "Quarter(s)"),
            ("semesterly", "Semester(s)"),
            ("yearly", "Year(s)"),
        ],
        default="monthly",
        string="Recurrence",
        help="Specify Interval for automatic invoice generation.",
        required=True
    )

    @api.model
    def new_contract(self, data_list):
        admin = self.env['res.users'].search([('login', '=', 'admin')], limit=1)
        for vals in data_list:
            # contract
            contract_vals= {}
            date_start = vals.get('date_start')
            date_end = vals.get('date_end')
            contract_vals['date_start'] = date_start
            contract_vals['date_end'] = date_end
            contract_vals['name'] = vals.get('name')
            contract_vals['structured_comm'] = vals.get('structured_comm')
            contract_vals['payment_mode'] = vals.get('payment_mode')
            contract_vals['recurring_rule_type'] = vals.get('recurring_rule_type')
            contract_vals['partner_id'] = admin.id

            contract_id = self.create(contract_vals)
            line_vals = {
                'record_id': contract_id,
                'date_start': date_start,
                'date_end': date_end,
                
            }
            for contract in vals.get('contracts'):
                #contract[]
                print(line_vals)
            # loop create contract
            # create first invoice
        return True