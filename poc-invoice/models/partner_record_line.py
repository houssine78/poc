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

    def _prepare_invoice_line_values(self, move_form):
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
                "price_unit": self.amount,
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
        # premium_scheme = premium_schem_obj.search([('record_line_id', '=', self.id)])
        if len(self.premium_scheme) > 0:
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

        max = len(matrix)-1
        for month in MONTH_KEYS:
            i=0
            j=1
            while i < max:
                if matrix[i][0][month] > 0.0:
                    if matrix[j][0][month] > 0.0:
                        vals[month] += matrix[i][0][month] - matrix[j][0][month]
                        if matrix[j][0]['invoiced'] == True:
                            break
                    elif j < max:
                        j+=1
                i+=1
        return vals
                    

    def action_invoice(self):
        # TODO add a check function to check
        # if all the line have a premium scheme
        # return user error otherwise
        if self.invoiced:
            raise ValidationError(_("Line already invoiced"))
        vals = self.compute_premium_scheme_amount()
        amount = sum(vals.values())
        return True
        

class InsurancePremiumScheme(models.Model):
    _name = 'premium.scheme'

    record_line_id = fields.Many2one('partner.record.line')
    partner_record_id = fields.Many2one('partner.record', related='record_line_id.record_id', store=True)
    product_id = fields.Many2one('product.product', related='record_line_id.product_id')
    start_date = fields.Date(related='record_line_id.start_date')
    end_date = fields.Date(related='record_line_id.end_date')
    invoiced = fields.Boolean(related='record_line_id.invoiced')
    january = fields.Float()
    february = fields.Float()
    march = fields.Float()
    april = fields.Float()
    may = fields.Float()
    june = fields.Float()
    july = fields.Float()
    august = fields.Float()
    september = fields.Float()
    october = fields.Float()
    november = fields.Float()
    december = fields.Float()
