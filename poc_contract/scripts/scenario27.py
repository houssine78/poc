import xmlrpc.client

url = "http://localhost:8014"
db = "poc_solidaris"
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
fin_moves = models.execute_kw(db, uid, password, 'contract.contract', 'get_financial_moves', [[
    {
    'contract': '0000199',
    'date_from': '2021-01-01',
    'date_to': '2021-12-31',
    },
]])
print(common.version())
print(uid)
print(fin_moves)
