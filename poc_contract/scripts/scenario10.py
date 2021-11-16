import xmlrpc.client

url = "http://localhost:8014"
db = "poc_solidaris"
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
ids = models.execute_kw(db, uid, password, 'contract.contract', 'new_contract', [[
    {
    'partner_name': 'Jean-Michel Saive',
    'partner_bank': 'BE60 3211 1234 7570',
    'partner_bic': 'BBRUBEBB',
    'name': '0000286',
    'structured_comm': '770000028624',
    'date_start': '2021-03-01',
    'date_end': '2021-12-31',
    'date_request': '2021-02-15',
    'recurring_rule_type': 'quarterly',
    'payment_mode': 'transfer',
    'total': 232.04,
    'contracts':[
        {
            'contract_ref': '000028601',
            'insurance': 'AHI option 150',
            'tax': '10%',
            'annual_amount': 144.00,
            'annual_amount_texcl': 130.91,
            'tax_amount': 13.09,
            'recurring_amount': 32.73,
            'recurring_tax': 3.27,
            'recurring_delta_texcl': -0.01,
            'recurring_delta': 0.01,
            'total_delta': 0.00
        },
        {
            'contract_ref': '000028602',
            'insurance': 'LCH',
            'tax': '10%',
            'annual_amount': 84.00,
            'annual_amount_texcl': 76.36,
            'tax_amount': 7.64,
            'recurring_amount': 19.09,
            'recurring_tax': 7.91,
            'recurring_delta_texcl': 0.00,
            'recurring_delta': 0.00,
            'total_delta': 0.00
        },
        {
            'contract_ref': '000028603',
            'insurance': 'MG',
            'tax': '9,25%',
            'annual_amount': 4.04,
            'annual_amount_texcl': 3.70,
            'tax_amount': 0.34,
            'recurring_amount': 0.92,
            'recurring_tax': 0.08,
            'recurring_delta_texcl': 0.02,
            'recurring_delta': 0.02,
            'total_delta': 0.04
        }]
    },
]])
print(common.version())
print(uid)
print(ids)
