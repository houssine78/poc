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
    'name': 'ext_007',
    'date': '2021-04-16',
    'balance_start': 579.45,
    'balance_end_real': 658.84,
    'lines':[
        {
            'date': '2021-04-15',
            'payment_ref': '+++770/0000/28624+++',
            'transaction_type': 'Simple amount without detailed data: Domestic or local SEPA credit transfers (Individual transfer order)',
            'amount': 79.39,
            'account_number': 'BE98 2333 3311 1693',
        }]
    },
]])
print(common.version())
print(uid)
print(ids)
