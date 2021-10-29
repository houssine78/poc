import xmlrpc.client

url = "http://localhost:8014"
db = "poc_solidaris"
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
ids = models.execute_kw(db, uid, password, 'contract.contract', 'request_payment_out', [[
    {
    'contract': '0000199',
    'date_request': '2021-04-18',
    'amount': 56.00,
    'account_number': 'FR3217569000501378382981T41',
    'partner_type': 'supplier'
    },
    {
    'contract': '0000286',
    'date_request': '2021-04-18',
    'amount': 423.00,
    'account_number': 'BE60 3211 1234 7570',
    'partner_type': 'supplier'
    },
]])
print(common.version())
print(uid)
print(ids)
