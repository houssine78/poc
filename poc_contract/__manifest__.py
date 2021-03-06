# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'POC Contract',
    'version': '14.0.1.0.8',
    'author': 'Eezee-It',
    'website': 'http://www.eezee-it.com',
    'category': 'Account',
    'license': 'LGPL-3',
    'depends': [
        'contacts',
        'account_accountant',
        'l10n_be',
        'contract',
        'account_sepa',
        'account_sepa_direct_debit'
    ],
    'data': [
        "data/poc_data.xml",
        "views/contract_views.xml",
        "views/contract_line.xml",
        "views/bank_statement_view.xml"
    ],
    'installable': True,
}
