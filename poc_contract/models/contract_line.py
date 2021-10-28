# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    contract_ref = fields.Char(string="Contract reference")
    annual_amount = fields.Float()
    annual_amount_texcl = fields.Float()
    tax = fields.Float()
    tax_amount = fields.Float()
    recurring_tax = fields.Float()
    recurring_delta_texcl = fields.Float()
    recurring_delta = fields.Float()
    total_delta = fields.Float()

    def _prepare_first_invoice_line(self, dates, ratio, move_form):
        self.ensure_one()
        line_form = move_form.invoice_line_ids.new()
        line_form.display_type = self.display_type
        line_form.product_id = self.product_id
        invoice_line_vals = line_form._values_to_save(all_fields=True)
        name = self._insert_markers(dates[0], dates[1])
        invoice_line_vals.update(
            {
                "account_id": invoice_line_vals["account_id"]
                if "account_id" in invoice_line_vals and not self.display_type
                else False,
                "quantity": 1,
                "product_uom_id": self.uom_id.id,
                "discount": self.discount,
                "contract_line_id": self.id,
                "sequence": self.sequence,
                "name": name,
                "analytic_account_id": self.analytic_account_id.id,
                "analytic_tag_ids": [(6, 0, self.analytic_tag_ids.ids)],
                "price_unit": self.price_unit * ratio,
            }
        )
        return invoice_line_vals
