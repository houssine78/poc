# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.tools import date_utils
from dateutil.relativedelta import relativedelta


class ContractContract(models.Model):
    _inherit = "contract.contract"

    structured_comm = fields.Char(string="Structured communication", required=True)
    payment_mode = fields.Selection([
        ('transfer', 'Wire transfer'),
        ('mandate', 'Mandate')],
        required=True
    )
    recurring_rule_type = fields.Selection(
        [
            ("monthly", "Month(s)"),
            ("quarterly", "Quarter(s)"),
            ("semesterly", "Semester(s)"),
            ("yearly", "Year(s)"),
        ],
        default="monthly",
        string="Recurrence",
        help="Specify Interval for automatic invoice generation.",
        required=True
    )

    @api.model
    def get_month_from_contract_period(self):
        if self.recurring_rule_type == "monthly":
            months = 1
        elif self.recurring_rule_type == "quarterly":
            months = 3
        elif self.recurring_rule_type == "semesterly":
            months = 6
        elif self.recurring_rule_type == "yearly":
            months = 12
        return months

    @api.model
    def get_period_from_contract(self):
        if self.recurring_rule_type == "monthly":
            period = "month"
        elif self.recurring_rule_type == "quarterly":
            period = "quarter"
        elif self.recurring_rule_type == "semesterly":
            period = "semester"
        elif self.recurring_rule_type == "yearly":
            period = "year"
        return period

    def _prepare_first_invoices_values(self, dates, ratio, date_ref=False):
        """
        This method builds the list of invoices values to create, based on
        the lines to invoice of the contracts in self.
        :return: list of dictionaries (invoices values)
        """
        invoices_values = []
        for contract in self:
            if not date_ref:
                date_ref = contract.recurring_next_date
            if not date_ref:
                # this use case is possible when recurring_create_invoice is
                # called for a finished contract
                continue
            contract_lines = contract._get_lines_to_invoice(date_ref)
            if not contract_lines:
                continue
            invoice_vals, move_form = contract._prepare_invoice(date_ref)
            invoice_vals["invoice_line_ids"] = []
            for line in contract_lines:
                invoice_line_vals = line._prepare_first_invoice_line(dates, ratio, move_form=move_form)
                if invoice_line_vals:
                    # Allow extension modules to return an empty dictionary for
                    # nullifying line. We should then cleanup certain values.
                    del invoice_line_vals["company_id"]
                    del invoice_line_vals["company_currency_id"]
                    invoice_vals["invoice_line_ids"].append((0, 0, invoice_line_vals))
            invoices_values.append(invoice_vals)
            # Force the recomputation of journal items
            del invoice_vals["line_ids"]
        return invoices_values

    def _create_first_invoice(self, dates, ratio, date_ref=False):
        invoices_values = self._prepare_first_invoices_values(dates, ratio, date_ref)
        moves = self.env["account.move"].create(invoices_values)
        self._invoice_followers(moves)
        return moves

    @api.model
    def next_period_first_day(self, period):
        next_period = self.date_start + self.get_relative_delta(self.recurring_rule_type, 1)
        return date_utils.start_of(next_period, period)

    def diff_month(self, d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month

    @api.model
    def first_invoicing(self, request_date):
        # find next period based on the recurrency
        date_start = self.date_start
        date_next_period = date_start + self.get_relative_delta(self.recurring_rule_type, 1)
        period = self.get_period_from_contract()
        next_period_fd = self.next_period_first_day(period)
        next_period_ld = date_utils.end_of(next_period_fd, period)

        # compute pro-rata ratio for contract lines
        if date_start != self.recurring_next_date or date_next_period == next_period_fd:
            ratio = 1
        else:
            # compute delta between start date and next period
            start_period = date_utils.start_of(date_start, period)
            delta_period = self.diff_month(next_period_fd, start_period)
            delta_start_date = self.diff_month(next_period_fd, date_start)
            ratio = delta_start_date / delta_period
        dates = [date_start, next_period_fd - relativedelta(days=1)]
        # create first invoice
        invoice = self._create_first_invoice(dates, ratio, fields.Date.today())

        self.recurring_next_date = next_period_fd
        lines_vals = {
            'next_period_date_start': next_period_fd,
            'next_period_date_end': next_period_ld,
            'recurring_next_date': next_period_fd,
            #'last_date_invoiced': request_date
        }
        self.contract_line_ids.write(lines_vals)
        
        return invoice

    @api.model
    def create_bank(self, data_list):
        bank_obj = self.env['res.bank']
        bank_obj.create({'name': 'Fortis Bank SA/NV', 'bic': 'GEBABEBB'})
        bank_obj.create({'name': 'ING Belgium SA/NV', 'bic': 'BBRUBEBB'})
        bank_obj.create({'name': 'KBC BANK NV', 'bic': 'KREDBEBB'})
        bank_obj.create({'name': 'COMPAGNIE MONEGASQUE DE BANQUE S.A.M', 'bic': 'CMBMMCMXXXX'})
        return True

    @api.model
    def new_contract(self, data_list):
        product_obj = self.env['product.product']
        line_obj = self.env['contract.line']
        partner_obj = self.env['res.partner']
        partner_bank_obj = self.env['res.partner.bank']
        bank_obj = self.env['res.bank']
        bank_journal = self.env['account.journal'].search([('type', '=', 'bank'), ('name', '=', 'Bank')], limit=1)
        payment_term = self.env.ref("account.account_payment_term_30days")

        for vals in data_list:
            # contract
            contract_vals= {}
            partner_vals = {}
            partner_bank_vals = {}
            
            # create partner
            partner_vals['name'] = vals.get('partner_name')
            partner_vals['ref'] = vals.get('structured_comm')[:-2]
            partner_vals['customer_rank'] = 1
            partner_vals['property_payment_term_id'] = payment_term.id
            partner = partner_obj.create(partner_vals)
            bank = bank_obj.search([('bic', '=', vals.get('partner_bic'))], limit=1)

            # create bank partner
            partner_bank_vals['partner_id'] = partner.id
            partner_bank_vals['acc_number'] = vals.get('partner_bank')
            partner_bank_vals['bank_id'] = bank.id
            partner_bank = partner_bank_obj.create(partner_bank_vals)
            
            # contract
            date_start = vals.get('date_start')
            date_end = vals.get('date_end')
            request_date = vals.get('date_request')
            contract_vals['date_start'] = date_start
            contract_vals['date_end'] = date_end
            contract_vals['name'] = vals.get('name')
            contract_vals['structured_comm'] = vals.get('structured_comm')
            contract_vals['payment_mode'] = vals.get('payment_mode')
            contract_vals['recurring_rule_type'] = vals.get('recurring_rule_type')
            contract_vals['partner_id'] = partner.id

            contract = self.create(contract_vals)
            line_vals = {
                'contract_id': contract.id,
                'date_start': date_start,
                'date_end': date_end,
                'is_auto_renew': True,
                'recurring_rule_type': vals.get('recurring_rule_type')
            }
            for contract_vals in vals.get('contracts'):
                insurance = contract_vals.get('insurance')
                product = product_obj.search([('default_code', '=', insurance)])
                line_vals['product_id'] = product.id
                line_vals['name'] = 'from #START# to #END#'
                line_vals['contract_ref'] = contract_vals.get('contract_ref')
                line_vals['tax'] = contract_vals.get('tax')
                line_vals['annual_amount'] = contract_vals.get('annual_amount')
                line_vals['annual_amount_texcl'] = contract_vals.get('annual_amount_texcl')
                line_vals['tax_amount'] = contract_vals.get('tax_amount')
                line_vals['price_unit'] = contract_vals.get('recurring_amount')
                line_vals['recurring_tax'] = contract_vals.get('recurring_tax')
                line_vals['recurring_delta_texcl'] = contract_vals.get('recurring_delta_texcl')
                line_vals['recurring_delta'] = contract_vals.get('recurring_delta')
                line_vals['total_delta'] = contract_vals.get('total_delta')
                line_obj.create(line_vals)
            
            if contract.payment_mode == 'mandate':
                # create sepa debit mandate
                mandate_vals = {}
                mandate_vals['partner_id'] = partner.id
                mandate_vals['partner_bank_id'] = partner_bank.id
                mandate_vals['payment_journal_id'] = bank_journal.id
                mandate_vals['start_date'] = request_date
                mandate = self.env['sdd.mandate'].create(mandate_vals)
                mandate.action_validate_mandate()
                
            # create first invoice
            invoice = contract.first_invoicing(request_date)
            invoice.invoice_date = request_date
            invoice.action_post()

        return True

    @api.model
    def request_payment(self, data_list):
        wiz_obj = self.env['account.payment.register']
        batch_obj = self.env['account.batch.payment']

        payment_method = self.env['account.payment.method'].search([('code', '=', 'sdd')], limit=1)
        bank_journal = self.env['account.journal'].search([('type', '=', 'bank'), ('name', '=', 'Bank')], limit=1)
        contracts = self.env['contract.contract'].search([('payment_mode', '=', 'mandate')])

        ctx = {'active_model': 'account.move'}
        request_date = data_list[0].get('request_date')
        reference_date = fields.Date().to_date(data_list[0].get('reference_date'))
        payments = []
        
        for contract in contracts:
            invoices = (self.env["account.move.line"].search([("contract_line_id", "in", contract.contract_line_ids.ids)]).mapped("move_id"))
            not_paid_inv = invoices.filtered(lambda l: l.payment_state == 'not_paid' and l.invoice_date <= reference_date)
            for inv in not_paid_inv:
                pay_vals = {}
                pay_vals['payment_method_id'] = payment_method.id
                pay_vals['journal_id'] = bank_journal.id
                pay_vals['payment_date'] = request_date
                
                ctx['active_ids']= inv.id
                wizard = wiz_obj.with_context(ctx).create(pay_vals)
                payment = wizard.create_payments()
                payments.append(payment.id)

        if payments:
            batch_vals = {}
            batch_vals['journal_id'] = bank_journal.id
            batch_vals['payment_method_id'] = payment_method.id
            batch_vals['date'] = request_date
    
            batch = batch_obj.create(batch_vals)
            batch.write({'payment_ids': [(6, 0, payments)]})
            batch.validate_batch()
            return True
        else:
            return "There is nothing to pay"

    @api.model
    def request_payment_out(self, data_list):
        payment_obj = self.env['account.payment']
        contract_obj = self.env['contract.contract']
        account_obj = self.env['account.account']

        account_dict = {}
        account_dict['supplier'] = account_obj.search([('code', '=', '440000')], limit=1)
        account_dict['customer'] = account_obj.search([('code', '=', '400000')], limit=1)

        payment_method = self.env['account.payment.method'].search([('code', '=', 'sepa_ct')], limit=1)
        bank_journal = self.env['account.journal'].search([('type', '=', 'bank'), ('name', '=', 'Bank')], limit=1)

        for request_payment in data_list:
            pay_vals = {}
            contract = contract_obj.search([('name', '=', request_payment.get('contract'))])
            pay_vals['partner_id'] = contract.partner_id.id
            pay_vals['payment_method_id'] = payment_method.id
            pay_vals['journal_id'] = bank_journal.id
            pay_vals['date'] = request_payment.get('date_request')
            pay_vals['payment_type'] = 'outbound'
            pay_vals['partner_type'] = request_payment.get('partner_type')
            pay_vals['amount'] = request_payment.get('amount')
            pay_vals['destination_account_id'] = account_dict.get(request_payment.get('partner_type')).id
            
            payment_obj.create(pay_vals)
        
        return True

    @api.model
    def batch_payment_out(self, data_list):
        payment_obj = self.env['account.payment']
        batch_obj = self.env['account.batch.payment']

        payment_method = self.env['account.payment.method'].search([('code', '=', 'sepa_ct')], limit=1)
        bank_journal = self.env['account.journal'].search([('type', '=', 'bank'), ('name', '=', 'Bank')], limit=1)
        domain_filter = [('state', '=', 'draft'), ('is_internal_transfer', '=', False)]

        batch_vals = {}
        batch_vals['journal_id'] = bank_journal.id
        batch_vals['payment_method_id'] = payment_method.id
        batch_vals['date'] = data_list[0].get('date')
        batch_vals['batch_type'] = 'outbound'
        
        batch = batch_obj.create(batch_vals)
        payments = payment_obj.search(domain_filter)
        batch.write({'payment_ids': [(6, 0, payments.ids)]})
        batch.validate_batch()

        return True

    @api.model
    def import_bank_statement(self, data_list):
        stat_obj = self.env['account.bank.statement']
        stat_line_obj = self.env['account.bank.statement.line']


        bank_journal = self.env['account.journal'].search([('type', '=', 'bank'), ('name', '=', 'Bank')], limit=1)
        
        for vals in data_list:
            stat_vals = {}
            stat_vals['name'] = vals.get('name')
            stat_vals['journal_id'] = bank_journal.id
            stat_vals['date'] = vals.get('date')
            stat_vals['balance_start'] = vals.get('balance_start')
            stat_vals['balance_end_real'] = vals.get('balance_end_real')
            statement = stat_obj.create(stat_vals)
            line_vals = {'statement_id': statement.id}
            for line in vals.get('lines'):
                line_vals['date'] = line.get('date')
                line_vals['payment_ref'] = line.get('payment_ref')
                line_vals['amount'] = line.get('amount')
                line_vals['account_number'] = line.get('account_number')
                stat_line_obj.create(line_vals)
            statement.button_post()
        return True

    def update_tax_on_invoice_lines(self, invoice):
        account = self.env['account.account'].search([('code', '=', '400000')], limit=1)
        debit_line = invoice.line_ids.filtered(lambda l: l.account_id.id == account.id)
        for inv_line in invoice.line_ids:
            if inv_line.tax_group_id:
                taxes = sum(self.contract_line_ids.filtered(lambda l: l.tax == inv_line.name).mapped('recurring_tax'))
                if taxes > 0:
                    diff = taxes - inv_line.credit
                    invoice.write({'line_ids':[
                            (1, inv_line.id, {'credit': taxes}),
                            (1, debit_line.id, {'debit': debit_line.debit + diff})
                        ]}
                    )
        return True
            
    @api.model
    def run_contract_invoicing(self, data_list):
        contract_obj = self.env['contract.contract']
        
        for vals in data_list:
            contract = contract_obj.search([('name', '=', vals.get('contract'))])
            invoice = contract.recurring_create_invoice()
            contract.update_tax_on_invoice_lines(invoice)
            invoice.action_post()

        return True

    def reverse_invoice(self, move_id, date):
        wiz_obj = self.env['account.move.reversal']
        ctx = {
                'active_model': 'account.move',
                'active_ids': move_id
            }
        cred_note_vals = {
                'refund_method': 'cancel',
                'reason': "plan d'appurement",
                'date_mode': 'custom',
                'date': date
            }
        wizard = wiz_obj.with_context(ctx).create(cred_note_vals)
        return wizard.reverse_moves()

    def create_clearance(self, contract, data_list):
        move_obj = self.env['account.move']
        line_obj = self.env['account.move.line']
        product_obj = self.env['product.product']
        account_obj = self.env['account.account']

        name = data_list.get('name')
        date = data_list.get('date')
        account = account_obj.search([('code', '=', '7000')])
        invoices = []
        for vals in data_list.get('invoices'):
            due_date = vals.get('due_date')
            inv_vals = {
                'invoice_date_due': due_date,
                'partner_id': contract.partner_id.id,
                'invoice_date': date,
                'move_type': 'out_invoice'
            }
            
            invoice = move_obj.create(inv_vals)
            line_vals = {'move_id': invoice.id}

            for line in vals.get('lines'):
                product = product_obj.search([('default_code', '=', line.get('insurance'))])
                line_vals['account_id'] = account.id
                line_vals['quantity'] = 1
                line_vals['product_uom_id'] = product.uom_id.id
                line_vals['product_id'] = product.id 
                line_vals['currency_id'] = contract.currency_id.id
                line_vals['name'] = name
                line_vals['discount'] = 0.0
                line_vals['display_type'] = False
                move_line = line_obj.new(line_vals)
                move_line._onchange_product_id()
                move_line.price_unit = line.get('amount')
                invoice.invoice_line_ids += move_line

            invoice._move_autocomplete_invoice_lines_values()
            invoice.action_post()
            invoices.append(invoice)
                        
        return invoices

    @api.model
    def invoice_clearance(self, data_list):
        contract_obj = self.env['contract.contract']

        contract_ref = data_list[0].get('name')

        contract = contract_obj.search([('name', '=', contract_ref)])
        invoices = contract._get_related_invoices()
        open_invoice = invoices.filtered(lambda inv: inv.state == 'posted' and inv.payment_state == 'not_paid')
        
        if len(open_invoice) > 0:
            date = data_list[0].get('date')
            self.reverse_invoice(open_invoice.id, date)

            self.create_clearance(contract, data_list[0])

        return True

    @api.model
    def get_financial_moves(self, data_list):
        contract_obj = self.env['contract.contract']
        move_line_obj = self.env['account.move.line']
        domain_filter = [
            ('move_id.state', '=', 'posted'),
            ('full_reconcile_id', '=', False),
            ('balance', '!=', 0),
            ('account_id.reconcile', '=', True)
        ]
        res = []
        for vals in data_list:
            contract = contract_obj.search([('name', '=', vals.get('contract'))])
            partner = contract.partner_id
            domain_filter.append(('partner_id', '=', partner.id))
            lines = move_line_obj.search(domain_filter)
            res.append(["Client", "Date", "Journal Entry", "Compte", "Label", "Echeance", "Debit", "Credit", "Balance"])
            for line in lines:
                res.append([line.partner_id.name, line.date, line.move_id.name, line.account_id.name, line.name, line.date_maturity, line.debit, line.credit, line.balance])
        return res
        
    def _create_invoice(self, name, date, move_type, amount, product_ref, contract_line, ratio=1):
        move_obj = self.env['account.move']
        line_obj = self.env['account.move.line']
        product_obj = self.env['product.product']
        account_obj = self.env['account.account']
        product = product_obj.search([('default_code', '=', product_ref)])

        account = account_obj.search([('code', '=', '7000')])

        inv_vals = {
            'partner_id': self.partner_id.id,
            'invoice_date': date,
            'move_type': move_type
        }
        
        invoice = move_obj.create(inv_vals)
        line_vals = {'move_id': invoice.id}

        line_vals['account_id'] = account.id
        line_vals['quantity'] = 1
        line_vals['product_uom_id'] = product.uom_id.id
        line_vals['product_id'] = product.id 
        line_vals['currency_id'] = self.currency_id.id
        line_vals['name'] = name
        line_vals['discount'] = 0.0
        line_vals['display_type'] = False
        line_vals['contract_line_id'] = contract_line.id
        move_line = line_obj.new(line_vals)
        move_line._onchange_product_id()
        move_line.price_unit = amount * ratio
        invoice.invoice_line_ids += move_line

        invoice._move_autocomplete_invoice_lines_values()
        invoice.action_post()
        return invoice

    @api.model
    def new_beneficiary(self, data_list):
        contract_obj = self.env['contract.contract']

        contract_ref = data_list[0].get('name')
        contract = contract_obj.search([('name', '=', contract_ref)])
        dates = 'from ' + data_list[0].get('date_start') + ' to ' + data_list[0].get('date_end')
        delta_invoicing = data_list[0].get('delta_invoicing_texcl')
        product_ref = False
        for data in data_list:
            for contract_line in data.get('contracts'):
                ref = contract_line.get('contract_ref')
                product_ref = contract_line.get('insurance')
                line = contract.contract_line_ids.filtered(lambda l: l.contract_ref == ref)
                vals = {
                    'tax': '10%',
                    'annual_amount': contract_line.get('annual_amount'),
                    'annual_amount_texcl': contract_line.get('annual_amount_texcl'),
                    'tax_amount': contract_line.get('tax_amount'),
                    'recurring_tax': contract_line.get('recurring_tax'),
                    'recurring_delta_texcl': contract_line.get('recurring_delta_texcl'),
                    'recurring_delta': contract_line.get('recurring_delta'),
                    'total_delta': contract_line.get('total_delta'),
                    'price_unit' : contract_line.get('annual_amount_texcl')
                }
                line.write(vals)
        contract._create_invoice(dates, fields.Date.today(), 'out_invoice', delta_invoicing, product_ref, line)
        
        return True

    @api.model
    def last_invoicing_ratio(self, date_stop):
        months = self.get_month_from_contract_period()
        period = self.get_period_from_contract()
        ongoing_period = date_utils.start_of(date_stop, period)
        month_in_period = date_stop.month - ongoing_period.month
        ratio = month_in_period / months

        return ratio

    @api.model
    def end_contract(self, data_list):
        contract_obj = self.env['contract.contract']

        #termination_reason = self.env.ref("termination_reason", False)
        termination_reason = self.env['contract.terminate.reason'].search([('name', '=', 'Contract resiliation')])

        contract_ref = data_list[0].get('name')
        comment  = data_list[0].get('commentaires')
        date_stop = fields.Date.to_date(data_list[0].get('date_end'))

        contract = contract_obj.search([('name', '=', contract_ref)])
        contract._terminate_contract(termination_reason, contract, date_stop)
        ratio = contract.last_invoicing_ratio(date_stop)
        line = contract.contract_line_ids[0]
        invoice = contract._create_invoice(contract_ref, fields.Date.today(), 'out_refund', line.price_unit, line.product_id.default_code, line, ratio)
        return True
