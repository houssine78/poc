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
    'name': 'ext_002',
    'date': '2021-02-15',
    'balance_start': 15.67,
    'balance_end_real': 385.82,
    'lines':[
        {
            'date': '2021-02-13',
            'payment_ref': '+++770/0000/19934+++ ',
            'amount': 15.67,
            'account_number': 'FR3217569000501378382981T41',
        },
        {
            'date': '2021-02-14',
            'payment_ref': '+++770/0000/20237+++ ',
            'amount': 354.48,
            'account_number': 'BE20 8681 2345 6756',
        }]
    },
]])
print(common.version())
print(uid)
print(ids)
