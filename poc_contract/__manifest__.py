# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - admin@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Solidaris Contract',
    'version': '14.0.1.0.1',
    'author': 'Eezee-It',
    'website': 'http://www.eezee-it.com',
    'category': 'Account',
    'license': 'LGPL-3',
    'depends': [
        'contract',
    ],
    'data': [
        "security/ir.model.access.csv",
        "data/poc_data.xml",
        "views/contract_views.xml",
        "views/partner_record_views.xml"
    ],
    'installable': True,
}
