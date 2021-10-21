# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class PartnerRecord(models.Model):
    _name = "partner.record"

    name = fields.Char(string="Partner record ref")
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
