# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.tools import date_utils


class PartnerRecordLine(models.Model):
    _name = "partner.record.line"

    product_id = fields.Many2one('product.product', required=True)
    record_id = fields.Many2one('partner.record', required=True)
    amount = fields.Float()
    start_date = fields.Date()
    end_date = fields.Date()

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
                # "product_uom_id": self.uom_id.id,
                "record_line_id": self.id,
#                "name": name,
                "price_unit": self.amount,
            }
        )
        return invoice_line_vals
