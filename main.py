import demeter
import mngDB

def message(channel,text):
    if channel == 0:
        print(text)
def evaluate(test,results):
    output=test
    for i in range(0,len(results)):
        output=output.replace("#"+str(i+1),results[i])
    return output
def normalize(text,char):
    i = 0
    messtmp=text.split(char)
    for mest in messtmp:
        mest = mest[0:25]
        mest = mest.ljust(25, ' ')
        messtmp[i] = mest
        i += 1
    return char.join(messtmp)

ddbb = mngDB.mngdb('demeter.sqlite')

query="select idcustomer,region,database,bucket,path,profile_name,brand from customers;"
customers=ddbb.execute(query)

query="select idcheck,query,warning,header,legend,message,applyto,notapplyto from checks;"
checks=ddbb.execute(query)

channel=0
warnings={}

for customer in customers:
    message(channel, "")
    message(channel, "")
    message(channel,"------------------------------------")
    message(channel,"procesando cliente: "+customer[0])
    message(channel,"------------------------------------")
    message(channel,"")
    warnings[customer[0]]=0
    params = {
        'region': customer[1],
        'database': customer[2],
        'bucket': customer[3],
        'path': customer[4],
        'query': ''
    }
    client = demeter.session(region_name=params["region"],profile_name=customer[5])

    for check in checks:
        if check[6] == "*":
            applyto=True
        elif customer[0] in check[6].split(','):
            applyto=True
        else:
            applyto=False
        if check[7]!="" and customer[0] in check[7].split(','):
            applyto = False
        if applyto:
            message(channel,"Check "+str(check[0])+":")
            params['query']=check[1].replace("#d",customer[2])
            params['query'] = params['query'].replace("#b", customer[6])
            result = demeter.athena_query_result(client, params)
            if result != False:
                evaluation=evaluate(check[2],result[0])
                header=evaluate(check[3],result[0])
                if evaluation!="":
                    warning=eval(evaluation)
                else:
                    warning=False
                if warning:
                    message(channel,"\tWARNING!!!!!:"+evaluation)
                    warnings[customer[0]] += 1
                elif evaluation!="":
                    message(channel, "\tevaluacion correcta:" + evaluation)
                message(channel, "\t" + header)
                if check[4] != "":
                    mess = normalize(check[4], ":")
                    message(channel, "\t\t" + mess)
                    message(channel, "\t\t" + "------------------------------------")
                for res in result:
                    mess=normalize(evaluate(check[5],res),":")
                    message(channel,"\t\t"+mess)
                message(channel, "")