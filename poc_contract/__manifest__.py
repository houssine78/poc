# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'POC Contract',
    'version': '14.0.1.0.2',
    'author': 'Eezee-It',
    'website': 'http://www.eezee-it.com',
    'category': 'Account',
    'license': 'LGPL-3',
    'depends': [
        'l10n_be',
        'contract',
    ],
    'data': [
        "data/poc_data.xml",
        "views/contract_views.xml",
        "views/contract_line.xml",
    ],
    'installable': True,
}
