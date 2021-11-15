import xmlrpc.client

url = "http://localhost:8014"
db = "poc_solidaris"
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
ids = models.execute_kw(db, uid, password, 'contract.contract', 'invoice_clearance', [[
    {
    'name': '0000242',
    'date': '2021-04-18',
    'invoices':[
        {
            'due_date': '2021-05-01',
            'name': "plan d'appurement 1/3",
            'lines':[
                {
                    'contract_ref': '000024201',
                    'insurance': 'AHI option 200',
                    'tax': 10.0,
                    'amount': 93.64
                    },
                {
                    'contract_ref': '000024202',
                    'insurance': 'MG',
                    'tax': 9.25,
                    'amount': 4.57
                }
            ]
        },
        {
            'due_date': '2021-08-01',
            'name': "plan d'appurement 2/3",
            'lines':[
                {
                    'contract_ref': '000024201',
                    'insurance': 'AHI option 200',
                    'tax': 10.0,
                    'amount': 93.64
                    },
                {
                    'contract_ref': '000024202',
                    'insurance': 'MG',
                    'tax': 9.25,
                    'amount': 4.57
                }
            ]
        },
        {
            'due_date': '2021-11-01',
            'name': "plan d'appurement 3/3",
            'lines':[
                {
                    'contract_ref': '000024201',
                    'insurance': 'AHI option 200',
                    'tax': 10.0,
                    'amount': 94.49
                    },
                {
                    'contract_ref': '000024202',
                    'insurance': 'MG',
                    'tax': 9.25,
                    'amount': 4.57
                }
            ]
        }]
    }
]])
print(common.version())
print(uid)
print(ids)
