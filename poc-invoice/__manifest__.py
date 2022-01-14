# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'POC Invoice',
    'version': '14.0.1.0.0',
    'author': 'Eezee-It',
    'website': 'http://www.eezee-it.com',
    'category': 'Account',
    'license': 'LGPL-3',
    'depends': [
        'contacts',
        'account_accountant',
        'account_payment_term_extension',
        'l10n_be',
        'l10n_be_reports',
        'account_sepa',
        'account_sepa_direct_debit'
    ],
    'data': [
        "data/poc_data.xml",
        "security/ir.model.access.csv",
        "views/partner_record_view.xml"
    ],
    'installable': True,
}
