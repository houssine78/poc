# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    ref_date = fields.Date(string="Reference date")


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    record_line_id = fields.Many2one(
        "partner.record.line", string="Record Line", index=True
    )
