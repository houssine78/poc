# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


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
