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
    'partner_name': 'Nafissatou Thiam',
    'partner_bank': 'BE98 2333 3311 1693',
    'partner_bic': 'GEBABEBB',
    'name': '0000353',
    'structured_comm': '770000028624',
    'date_start': '2021-04-01',
    'date_end': '2021-12-31',
    'date_request': '2021-03-18',
    'recurring_rule_type': 'yearly',
    'payment_mode': 'transfer',
    'total': 92.52,
    'contracts':[
        {
            'contract_ref': '000035301',
            'insurance': 'AHI Base',
            'tax': 10,
            'annual_amount': 92.52,
            'annual_amount_texcl': 84.11,
            'tax_amount': 8.41,
            'recurring_amount': 84.11,
            'recurring_tax': 8.41,
            'recurring_delta_texcl': 0.00,
            'recurring_delta': 0.00,
            'total_delta': 0.00
        }]
    },
]])
print(common.version())
print(uid)
print(ids)
