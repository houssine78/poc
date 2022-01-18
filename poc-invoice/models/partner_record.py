# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.tools import date_utils
from odoo.tests import Form

class PartnerRecord(models.Model):
    _name = "partner.record"

    name = fields.Char()
    partner_id = fields.Many2one('res.partner', string="Customer")
    start_date = fields.Date()
    end_date = fields.Date()
    invoice_count = fields.Integer(compute="_compute_invoice_count")
    recurring_rule_type = fields.Selection(
        [
            ("monthly", "Month(s)"),
            ("quarterly", "Quarter(s)"),
            ("semesterly", "Semester(s)"),
            ("yearly", "Year(s)"),
        ],
        default="yearly",
        string="Recurrence",
        help="Specify Interval for automatic invoice generation.",
    )
    ongoing_record_lines = fields.One2many('partner.record.line', 'record_id', domain=[('end_date', '=', False)])
    old_record_lines = fields.One2many('partner.record.line', 'record_id', domain=[('end_date', '!=', False)])
    premium_scheme = fields.One2many('premium.scheme', 'partner_record_id') 

    def _get_related_invoices(self):
        self.ensure_one()

        invoices = (
            self.env["account.move.line"]
            .search(
                [
                    (
                        "record_line_id",
                        "in",
                        self.ongoing_record_lines.ids + self.old_record_lines.ids
                    )
                ]
            )
            .mapped("move_id")
        )
        return invoices

    def _prepare_invoice_values(self, invoice_date, ref_date=None, payment_term_id=None):
        self.ensure_one()
        move_obj = self.env['account.move']
        journal = self.env["account.journal"].search([("type", "=", 'sale')])
        move_form = Form(move_obj.with_context(default_move_type='out_invoice'))
        move_form.partner_id = self.partner_id

        if not payment_term_id:
            payment_term_id = self.partner_id.property_payment_term_id
        move_form.invoice_payment_term_id = payment_term_id
        if self.partner_id.property_account_position_id:
            move_form.fiscal_position_id = self.partner_id.property_account_position_id
        invoice_vals = move_form._values_to_save(all_fields=True)
        invoice_vals.update({
            'journal_id': journal.id,
            'invoice_date': invoice_date,
            'ref_date': ref_date
        })

        return invoice_vals, move_form

    def action_show_invoices(self):
        self.ensure_one()
        tree_view = self.env.ref("account.view_invoice_tree", raise_if_not_found=False)
        form_view = self.env.ref("account.view_move_form", raise_if_not_found=False)
        action = {
            "type": "ir.actions.act_window",
            "name": "Invoices",
            "res_model": "account.move",
            "view_mode": "tree,kanban,form,calendar,pivot,graph,activity",
            "domain": [("id", "in", self._get_related_invoices().ids)],
        }
        if tree_view and form_view:
            action["views"] = [(tree_view.id, "tree"), (form_view.id, "form")]
        return action

    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = len(rec._get_related_invoices())

    def create_invoice(self, invoice_date=None, ref_date=None):
        move_obj = self.env['account.move']
        invoices_values = []
        if not invoice_date:
            invoice_date = fields.Date().today()
        for record in self:
            invoice_vals, move_form = record._prepare_invoice_values(invoice_date)
            lines = record.ongoing_record_lines.filtered(lambda l: not l.invoiced)
            for line in lines:
                line_vals = line._prepare_invoice_line_values(move_form)
                invoice_vals["invoice_line_ids"].append((0, 0, line_vals))
                del invoice_vals["line_ids"]
            invoices_values.append(invoice_vals)
            move_obj.create(invoices_values)
            lines.write({'invoiced': True})
        return True
        