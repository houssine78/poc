# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    record_id = fields.Many2one('partner.record')
    representative_id = fields.Many2one(
        'res.partner',
        related='record_id.representative_id'
    )
