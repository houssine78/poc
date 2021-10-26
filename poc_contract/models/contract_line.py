# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    annual_amount = fields.Float()
    annual_amount_texcl = fields.Float()
    tax = fields.Float()
    recurring_tax = fields.Float()
    recurring_delta_texcl = fields.Float()
    recurring_delta = fields.Float()
    total_delta = fields.Float()
