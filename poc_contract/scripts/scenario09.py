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
    'balance_end_real': 90.42,
    'lines':[
        {
            'date': '2021-02-14',
            'payment_ref': 'Votre remise de domiciliation en euros (SEPA), total de 2 paiement(s)',
            'transaction_type': 'Simple amount without detailed data: Direct debit (Credit under usual reserve)',
            'amount': 74.75,
            'account_number': 'BE20 8681 2345 6756',
        }]
    },
]])
print(common.version())
print(uid)
print(ids)
