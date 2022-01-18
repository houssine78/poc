# Copyright 2021 Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class UpdateInsuranceAmount(models.TransientModel):
    _name = 'update.insurance.amount.wizard'
    _description = 'Update insurance amount wizard'

    amount = fields.Float()
    start_date = fields.Date()

    def process(self):
        self.ensure_one()

        record_line_obj = self.env['partner.record.line']
        line = record_line_obj.browse(self.env.context['active_id'])
        vals = {
            'amount': self.amount,
            'invoiced': False,
            'start_date': self.start_date,
            'previous_record_line_id': line.id
        }
        new_line = line.copy(vals)
        line.write({'end_date': self.start_date})

        new_line.create_prime_scheme()
        
        return True
        
