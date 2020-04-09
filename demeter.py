import boto3
import re
import time

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
# https://www.ilkkapeltola.fi/2018/04/simple-way-to-query-amazon-athena-in.html
# https://gist.github.com/schledererj/b2e2a800998d61af2bbdd1cd50e08b76

def session (region_name,profile_name):
    session = boto3.Session(profile_name=profile_name)
    client = session.client('athena', region_name=region_name)
    return client
def athena_query(client, params):
    try:
        response = client.start_query_execution(
            QueryString=params["query"],
            QueryExecutionContext={
                'Database': params['database']
            },
            ResultConfiguration={
                'OutputLocation': 's3://' + params['bucket'] + '/' + params['path']
            }
        )
        return response
    except:
        print("Error running query:"+params['query'])

def athena_query_result(client, params,max_execution = 5):
    execution = athena_query(client, params)
    execution_id = execution['QueryExecutionId']
    query_status = None
    while (max_execution > 0) and (query_status == 'QUEUED' or query_status == 'RUNNING' or query_status is None):
        max_execution = max_execution - 1
        query_status = client.get_query_execution(QueryExecutionId=execution_id)['QueryExecution']['Status']['State']
        if query_status == 'FAILED' or query_status == 'CANCELLED':
            #raise Exception('Athena query with the string "{}" failed or was cancelled'.format(query_string))
            print('Athena query with the string "{}" failed or was cancelled'.format(params['query']))
            return False
        time.sleep(10)
    if max_execution <= 0:
        print('Athena query with the string "{}" had timeout'.format(params['query']))
        return False
    results_paginator = client.get_paginator('get_query_results')
    results_iter = results_paginator.paginate(
        QueryExecutionId=execution_id,
        PaginationConfig={
            'PageSize': 1000
        }
    )
    results = []
    data_list = []
    for results_page in results_iter:
        for row in results_page['ResultSet']['Rows']:
            data_list.append(row['Data'])
    for datum in data_list[1:]:
        results.append([x['VarCharValue'] for x in datum])
    return results

def cleanup(session, params):
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(params['bucket'])
    for item in my_bucket.objects.filter(Prefix=params['path']):
        #item.delete()
        print(item)
