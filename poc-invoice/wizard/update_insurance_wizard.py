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
        #payment_term = self.env.ref('payment_term_dynamic')
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
        
        # date_invoice = fields.Date.today()
        # invoice_vals = new_insurance.record_id._prepare_invoice_values(date_invoice, self.start_date, payment_term)
        # line_vals = new_insurance._prepare_invoice_line_values(move_form)
        # invoice_vals["invoice_line_ids"].append((0, 0, line_vals))
        # del invoice_vals["line_ids"]
        # move_obj.create(invoice_values)
        #new_insurance.invoiced = True

        return True
        
