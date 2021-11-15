import xmlrpc.client

url = "http://localhost:8014"
db = "poc_solidaris"
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
ids = models.execute_kw(db, uid, password, 'contract.contract', 'new_beneficiary', [[
    {
    'name': '0000353',
    'date_start': '2021-06-01',
    'date_end': '2021-12-31',
    'date_request': '2021-05-01',
    'delta_invoicing': 45.36,
    'delta_invoicing_texcl': 41.24,
    'total': 170.28,
    'contracts':[
        {
            'contract_ref': '000035301',
            'insurance': 'AHI Base',
            'tax': 10,
            'annual_amount': 170.28,
            'annual_amount_texcl': 154.80,
            'tax_amount': 15.48,
            'recurring_amount': 170.28,
            'recurring_tax': 15.48,
            'recurring_delta_texcl': 0.00,
            'recurring_delta': 0.00,
            'total_delta': 0.00
        }]
    },
]])
print(common.version())
print(uid)
print(ids)
