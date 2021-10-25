# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class PartnerRecord(models.Model):
    _name = "partner.record"

    name = fields.Char(string="Partner record ref", required=True)
    active = fields.Boolean(default=True)
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
    contract_ids = fields.One2many(
        'contract.contract',
        'record_id',
        string="Contracts"
    )
    representative_id = fields.Many2one(
        'res.partner',
        string="Household representative",
        required=True
    )
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)

    @api.model
    def new_partner_record(self, data_list):
        admin = self.env['res.users'].search([('login', '=', 'admin')], limit=1)
        for vals in data_list:
            # create_partner_record
            rec_vals= {}
            rec_vals['name'] = vals.get('name')
            rec_vals['structured_comm'] = vals.get('structured_comm')
            rec_vals['payment_mode'] = vals.get('payment_mode')
            rec_vals['recurring_rule_type'] = vals.get('recurring_rule_type')
            rec_vals['date_start'] = vals.get('date_start')
            rec_vals['date_end'] = vals.get('date_end')
            rec_vals['representative_id'] = admin.id
            
            record_id = self.create(rec_vals)
            for contract in vals.get('contracts'):
                print(contract)
            # loop create contract
            # create first invoice
        return True
            