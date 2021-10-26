# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.tools import date_utils
from dateutil.relativedelta import relativedelta


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
    def get_period_from_contract(self):
        if self.recurring_rule_type == "monthly":
            period = "month"
        elif self.recurring_rule_type == "quarterly":
            period = "quarter"
        elif self.recurring_rule_type == "semesterly":
            period = "semester"
        elif self.recurring_rule_type == "yearly":
            period = "year"
        return period

    @api.model
    def next_period_first_day(self, period):
        next_period = self.date_start + self.get_relative_delta(self.recurring_rule_type, 1)
        return date_utils.start_of(next_period, period)

    @api.model
    def first_invoicing(self):
        # find next period based on the recurrency
        if self.date_start != self.recurring_next_date:
            return False
        period = self.get_period_from_contract()
        next_period_fd = self.next_period_first_day(period)
        date_next_period = self.date_start + self.get_relative_delta(self.recurring_rule_type, 1)
        if date_next_period == next_period_fd:
            return False

        # compute delta between start date and next period
        start_period = date_utils.start_of(self.date_start, period)
        delta_period = (next_period_fd - start_period).days
        delta = (next_period_fd - self.date_start).days
        # compute pro-rata amount for contract lines based on delta
        return delta

    @api.model
    def new_contract(self, data_list):
        admin = self.env['res.users'].search([('login', '=', 'admin')], limit=1)
        product_obj = self.env['product.product']

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
                'contract_id': contract_id.id,
                'date_start': date_start,
                'date_end': date_end,
                'is_auto_renew': True
            }
            for contract in vals.get('contracts'):
                insurance = contract.get('insurance')
                product = product_obj.search([('default_code', '=', insurance)])
                line_vals['product_id'] = product.id
                line_vals['name'] = 'lala'
                line_vals['contract_ref'] = contract.get('contract_ref')
                line_vals['tax'] = contract.get('tax')
                line_vals['annual_amount'] = contract.get('annual_amount')
                line_vals['annual_amount_texcl'] = contract.get('annual_amount_texcl')
                line_vals['tax_amount'] = contract.get('tax_amount')
                line_vals['price_unit'] = contract.get('recurring_amount')
                line_vals['recurring_tax'] = contract.get('recurring_tax')
                line_vals['recurring_delta_texcl'] = contract.get('recurring_delta_texcl')
                line_vals['recurring_delta'] = contract.get('recurring_delta')
                line_vals['total_delta'] = contract.get('total_delta')
                self.env['contract.line'].create(line_vals)
            contract_id.first_invoicing()
            # create first invoice
        return True