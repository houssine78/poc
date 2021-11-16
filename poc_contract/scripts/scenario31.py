import xmlrpc.client

url = "http://localhost:8014"
db = "poc_solidaris"
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
ids = models.execute_kw(db, uid, password, 'contract.contract', 'import_bank_statement', [[
    {
    'name': 'ext_09',
    'date': '2021-05-16',
    'balance_start': 381.77,
    'balance_end_real': 489.77,
    'lines':[
        {
            'date': '2021-05-15',
            'payment_ref': '',
            'amount': 108,
            'account_number': 'BE22 4565 4439 5147',
        }]
    },
]])
print(common.version())
print(uid)
print(ids)
