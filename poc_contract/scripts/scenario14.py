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
    'name': 'ext_003',
    'date': '2021-03-16',
    'balance_start': 90.42,
    'balance_end_real': 106.09,
    'lines':[
        {
            'date': '2021-03-14',
            'payment_ref': '+++770/0000/19934+++ ',
            'transaction_type': 'Simple amount without detailed data: Direct debit (Credit under usual reserve)',
            'amount': 15.67,
            'account_number': 'FR3217569000501378382981T41',
        }]
    },
]])
print(common.version())
print(uid)
print(ids)
