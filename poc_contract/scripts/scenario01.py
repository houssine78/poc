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
    'partner_name': 'Eden Hazard',
    'partner_bank': 'FR3217569000501378382981T41',
    'partner_bic': 'CMBMMCMXXXX',
    'name': '0000199',
    'structured_comm': '770000019934',
    'date_start': '2021-01-01',
    'date_end': '2021-12-31',
    'date_request': '2020-12-20',
    'recurring_rule_type': 'monthly',
    'payment_mode': 'mandate',
    'total': 188.09,
    'contracts':[
        {
            'contract_ref': '000019901',
            'insurance': 'AHI option 150',
            'tax': 10,
            'annual_amount': 170.88,
            'annual_amount_texcl': 155.35,
            'tax_amount': 15.53,
            'recurring_amount': 12.95,
            'recurring_tax': 1.29,
            'recurring_delta_texcl': -0.05,
            'recurring_delta': 0.05,
            'total_delta': 0.00
        },
        {
            'contract_ref': '000019902',
            'insurance': 'MG',
            'tax': 9.25,
            'annual_amount': 17.21,
            'annual_amount_texcl': 15.75,
            'tax_amount': 1.46,
            'recurring_amount': 1.31,
            'recurring_tax': 0.12,
            'recurring_delta_texcl': 0.03,
            'recurring_delta': 0.02,
            'total_delta': 0.05
        }]
    },
]])
print(common.version())
print(uid)
print(ids)
