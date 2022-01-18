# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tools import date_utils
from odoo import api, fields, models


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    payment_term_type = fields.Selection([('ref_date_endOfYear', 'On ref date and until and of the Year')])
    recurring_rule_type = fields.Selection(
        [
            ("monthly", "Month(s)"),
            ("quarterly", "Quarter(s)"),
            ("semesterly", "Semester(s)"),
            ("yearly", "Year(s)"),
        ],
        default="yearly",
        string="Recurrence",
        help="Specify Interval for payment term line generation.",
    )

    def compute_line_amount(self, type, value_amount, total_amount, remaining_amount, precision_digits):
        """Compute the amount for a payment term line.
        In case of procent computation, use the payment
        term line rounding if defined

            :param total_amount: total balance to pay
            :param remaining_amount: total amount minus sum of previous lines
                computed amount
            :returns: computed amount for this line
        """
        self.ensure_one()
        if type == "fixed":
            return float_round(value_amount, precision_digits=precision_digits)
        elif type in ("percent", "percent_amount_untaxed"):
            amt = total_amount * value_amount / 100.0
            if self.amount_round:
                amt = float_round(amt, precision_rounding=0.0)
            return float_round(amt, precision_digits=precision_digits)
        elif type == "balance":
            return float_round(remaining_amount, precision_digits=precision_digits)
        return None

    def compute(self, value, date_ref=False, currency=None):
        self.ensure_one()
        if self.payment_term_type != 'ref_date_endOfYear':
            return super(AccountPaymentTerm, self).compute(value, date_ref, currency)

        last_account_move = self.env.context.get("last_account_move", False)
        if last_account_move.date_ref:
            date_ref = last_account_move.date_ref
        else:
            date_ref = date_ref or fields.Date.today()
        amount = value
        result = []
        if not currency:
            if self.env.context.get("currency_id"):
                currency = self.env["res.currency"].browse(
                    self.env.context["currency_id"]
                )
            else:
                currency = self.env.company.currency_id
        precision_digits = currency.decimal_places
        next_date = fields.Date.from_string(date_ref)
        end_of_year = date_utils.enf_of(next_date, 'year')
        months = (end_of_year.month - next_date) + 1
        percentage = 100 / months
        for i in range(months):
            if i==months:
                amt = line.compute_line_amount('balance', percentage, value, amount, precision_digits)
                break
            amt = line.compute_line_amount('percent', percentage, value, amount, precision_digits)
            next_date += relativedelta(months=1)
            i=i+1

            next_date = self.apply_payment_days(line, next_date)
            next_date = self.apply_holidays(next_date)
            if not float_is_zero(amt, precision_digits=precision_digits):
                result.append((fields.Date.to_string(next_date), amt))
                amount -= amt
        amount = reduce(lambda x, y: x + y[1], result, 0.0)
        dist = round(value - amount, precision_digits)
        if dist:
            last_date = result and result[-1][0] or fields.Date.today()
            result.append((last_date, dist))
        return result