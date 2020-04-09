import mngDB
import json


ddbb = mngDB.mngdb('demeter.sqlite')

with open('./customers.json') as f:
  customers_dict= json.load(f)

for customer in customers_dict:
    # Create customers records
    params={}
    params['idcustomer'] = customer
    params['region'] = customers_dict[customer]['region']
    params['database'] = customers_dict[customer]['database']
    params['bucket'] = customers_dict[customer]['bucket']
    params['path'] = customers_dict[customer]['path']
    params['profile_name'] = customers_dict[customer]['profile_name']
    params['brand'] = customers_dict[customer]['brand']
    ddbb.execute("delete from customers where idcustomer='" + params['idcustomer'] + "';")
    ddbb.insert_dict("customers", params)

print(str(len(customers_dict))+" Customers recorded.")

with open('./checks.json') as f:
    checks_dict= json.load(f)

for check in checks_dict:
    test = {}
    test['idcheck'] = check
    test['query'] = checks_dict[check]['query']
    test['warning'] = checks_dict[check]['warning']
    test['header'] = checks_dict[check]['header']
    test['legend'] = checks_dict[check]['legend']
    test['message'] = checks_dict[check]['message']
    test['applyto'] = checks_dict[check]['applyto']
    test['notapplyto'] = checks_dict[check]['notapplyto']
    ddbb.execute("delete from checks where idcheck='" + test['idcheck'] + "';")
    ddbb.insert_dict("checks", test)

print(str(len(checks_dict))+" Checks recorded.")

exit()
