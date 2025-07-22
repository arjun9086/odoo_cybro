import xmlrpc.client

url_db1 = "http://cybrosys:8017"
db_1 = 'odoo_17'
username_db_1 = 'arjunn'
password_db_1 = 'cool'
common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
version_db1 = common_1.version()

url_db2 = "http://cybrosys:8018"
db_2 = 'odoo'
username_db_2 = 'walterwhite@gmail.com'
password_db_2 = 'cool'
common_2 = xmlrpc.client.ServerProxy('{ }/xmlrpc/2/common'.format(url_db2))
models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
version_db2 = common_2.version()

uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})

db_1_cust = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [[]],
                                {'fields': ['id', 'name', 'email', 'mobile'], 'limit': 1})

new_cust = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'create', [db_1_cust])
