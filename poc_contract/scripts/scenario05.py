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
    'partner_name': 'Philippe Gilbert',
    'partner_bank': 'BE22 4565 4439 5147',
    'partner_bic': 'KREDBEBB',
    'name': '0000242',
    'structured_comm': '770000024277',
    'date_start': '2021-02-01',
    'date_end': '2021-12-31',
    'date_request': '2021-01-15',
    'recurring_rule_type': 'yearly',
    'payment_mode': 'transfer',
    'total': 354.48,
    'contracts':[
        {
            'contract_ref': '000024201',
            'insurance': 'AHI option 200',
            'tax': 10,
            'annual_amount': 337.20,
            'annual_amount_texcl': 306.55,
            'tax_amount': 30.65,
            'recurring_amount': 306.55,
            'recurring_tax': 30.65,
            'recurring_delta_texcl': 0.00,
            'recurring_delta': 0.00,
            'total_delta': 0.00
        },
        {
            'contract_ref': '000024202',
            'insurance': 'MG',
            'tax': 9.25,
            'annual_amount': 17.28,
            'annual_amount_texcl': 15.82,
            'tax_amount': 1.46,
            'recurring_amount': 15.82,
            'recurring_tax': 1.46,
            'recurring_delta_texcl': 0.0,
            'recurring_delta': 0.00,
            'total_delta': 0.00
        }]
    },
]])
print(common.version())
print(uid)
print(ids)
