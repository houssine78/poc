import xmlrpc.client

url = "http://localhost:8014"
db = "poc_solidaris"
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
ids = models.execute_kw(db, uid, password, 'contract.contract', 'end_contract', [[
    {
    'name': '0000353',
    'date_end': '2021-07-01',
    'date_request': '2021-05-01',
    'commentaires': 'Changement de mutuelle'
    },
]])
print(common.version())
print(uid)
print(ids)
