# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, fields, models
from odoo.tools import date_utils
from odoo.exceptions import ValidationError

MONTH_KEYS = ['january', 'february', 'march', 'april', 'may',
              'june', 'july', 'august', 'september', 'october',
              'november', 'december']


class PartnerRecordLine(models.Model):
    _name = "partner.record.line"

    product_id = fields.Many2one('product.product', required=True)
    record_id = fields.Many2one('partner.record', required=True)
    amount = fields.Float()
    start_date = fields.Date()
    end_date = fields.Date()
    previous_record_line_id = fields.Many2one('partner.record.line', string="Previous record line")
    premium_schemes = fields.One2many('premium.scheme', 'record_line_id')
    invoiced = fields.Boolean()

    def _prepare_invoice_line_values(self, move_form, amount=None):
        self.ensure_one()
        line_form = move_form.invoice_line_ids.new()
        line_form.product_id = self.product_id
        invoice_line_vals = line_form._values_to_save(all_fields=True)
        invoice_line_vals.update(
            {
                "account_id": invoice_line_vals["account_id"]
                if "account_id" in invoice_line_vals
                else False,
                "quantity": 1,
                "record_line_id": self.id,
                "price_unit": amount,
            }
        )
        return invoice_line_vals

    def get_premium_scheme_vals(self, premium, start_date):
        vals = {'january':0.0, 'february':0.0, 'march':0.0, 'april':0.0, 'may':0.0,
              'june':0.0, 'july':0.0, 'august':0.0, 'september':0.0, 'october':0.0,
              'november':0.0, 'december':0.0}
        start = start_date.month - 1
        for i in range(start, 12):
            vals[MONTH_KEYS[i]] = premium
        return vals

    def create_prime_scheme(self):
        premium_schem_obj = self.env['premium.scheme']
        if len(self.premium_schemes) > 0:
            raise ValidationError(_("A premium scheme already exists for this line"))
        premium = self.amount / 12
        vals = self.get_premium_scheme_vals(premium, self.start_date)
        vals['record_line_id'] = self.id
        premium_schem_obj.create(vals)

        return True

    def compute_premium_scheme_amount(self):
        premium_schem_obj = self.env['premium.scheme']
        end_of_year = date_utils.end_of(fields.Date.today(), 'year')
        vals = self.get_premium_scheme_vals(0.0, end_of_year) 
        premium_schemes = premium_schem_obj.search([('partner_record_id', '=', self.record_id.id),('product_id', '=', self.product_id.id)], order='id desc')

        matrix = {}
        i = 0
        for premium_scheme in premium_schemes:
            matrix[i] = premium_scheme.read(MONTH_KEYS + ['invoiced'])
            i+=1

        # First invoice of the year case
        if len(matrix) == 1:
            for month in MONTH_KEYS:
                vals[month] += matrix[0][0][month]
            return vals

        limit = len(matrix)-1
        for month in MONTH_KEYS:
            i=0
            j=1
            while j <= limit:
                if matrix[i][0][month] > 0.0:
                    while j <= limit and matrix[j][0][month] == 0.0:
                        j+=1
                    if matrix[j][0][month] > 0.0:
                        vals[month] += matrix[i][0][month] - matrix[j][0][month]
                        if matrix[j][0]['invoiced'] == True:
                            break
                        
                i+=1
                j=i+1
        return vals
                    
    def action_invoice(self):
        # TODO add a check function to check
        # if all the line have a premium scheme
        # return user error otherwise
        if self.invoiced:
            raise ValidationError(_("Line already invoiced"))
        if not self.premium_schemes:
            self.create_prime_scheme()
        vals = self.compute_premium_scheme_amount()
        amount = sum(vals.values())

        payment_term = self.env.ref('poc-invoice.payment_term_dynamic')
        move_obj = self.env['account.move']
        date_invoice = fields.Date.today()
        invoice_vals, move_form = self.record_id._prepare_invoice_values(date_invoice, self.start_date, payment_term)
        line_vals = self._prepare_invoice_line_values(move_form, amount)
        invoice_vals["invoice_line_ids"].append((0, 0, line_vals))
        del invoice_vals["line_ids"]
        move_obj.create(invoice_vals)
        lines = self.search([('product_id', '=', self.product_id.id), ('id', '<=', self.id)])
        lines.write({'invoiced': True})
        return True
