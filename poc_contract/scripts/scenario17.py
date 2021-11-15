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
    'name': 'ext_004',
    'date': '2021-03-24',
    'balance_start': 106.09,
    'balance_end_real': 125.42,
    'lines':[
        {
            'date': '2021-03-20',
            'payment_ref': '+++770/0000/28624+++',
            'transaction_type': 'Simple amount without detailed data: Domestic or local SEPA credit transfers (Individual transfer order)',
            'amount': 19.33,
            'account_number': 'BE60 3211 1234 7570',
        }]
    },
]])
print(common.version())
print(uid)
print(ids)
