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
    'contract': '0000353',
    'date_request': '2021-04-20',
    'amount': 10.00,
    'account_number': 'BE98 2333 3311 1693',
    'partner_type': 'customer'
    },
]])
print(common.version())
print(uid)
print(ids)
