from __future__ import print_function

import json
import boto3


print('Loading function')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def myUpdate(x):
    bod={}
    Key={}
    ExpressionAttributeNames={}
    ExpressionAttributeValues = {}
    item = x.get('Item')
    Key["menu_id"]=item.get('menu_id')
    UpdateExpression = 'SET '
    needComma = False
    bod["Key"] = Key
    if("store_name" in item):
        ExpressionAttributeNames["#SN"]="store_name"
        ExpressionAttributeValues[":SNV"]=item.get("store_name")
        UpdateExpression  = UpdateExpression + "#SN = :SNV "
        needComma = True;
    if("selection" in item):
        ExpressionAttributeNames["#S"]="selection"
        ExpressionAttributeValues[":SV"]=item.get("selection")
        if(needComma):
            UpdateExpression = UpdateExpression + ", "
        UpdateExpression  = UpdateExpression + "#S = :SV "
        needComma = True;
    if("size" in item):
        ExpressionAttributeNames["#SZ"]="size"
        ExpressionAttributeValues[":SZV"]=item.get("size")
        if(needComma):
            UpdateExpression = UpdateExpression + ", "
        UpdateExpression  = UpdateExpression + "#SZ = :SZV "
        needComma = True;
    if("price" in item):
        ExpressionAttributeNames["#P"]="price"
        ExpressionAttributeValues[":PV"]=item.get("price")
        if(needComma):
            UpdateExpression = UpdateExpression + ", "
        UpdateExpression  = UpdateExpression + "#P = :PV "
        needComma = True;
    if("store_hours" in item):
        ExpressionAttributeNames["#SH"]="store_hours"
        ExpressionAttributeValues[":SHV"]=item.get("store_hours")
        if(needComma):
            UpdateExpression = UpdateExpression + ", "
        UpdateExpression  = UpdateExpression + "#SH = :SHV "
    bod["ExpressionAttributeNames"]=ExpressionAttributeNames
    bod["ExpressionAttributeValues"]=ExpressionAttributeValues
    bod["TableName"]="menu"
    #UpdateExpression = 'SET #SN = :SNV, #S = :SV, #SZ = :SZV, #P = :PV, #SH = :SHV'
    bod["UpdateExpression"]=UpdateExpression
    print (bod)
    return bod


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    #print("Received event: " + json.dumps(event, indent=2))
    
    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.get_item(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**myUpdate(x)),
    }

    responseBody = {
        'DELETE': lambda x: "200 OK" if x["statusCode"] == "200" else"ERROR",
        'GET': lambda x: x["body"]["Item"],
        'POST': lambda x: "200 OK" if x["statusCode"] == "200" else"ERROR",
        'PUT': lambda x: "200 OK" if x["statusCode"] == "200" else"ERROR",
    }

    operation = event['httpMethod']
    if operation in operations:
        payload = event['body']
        dynamo = boto3.resource('dynamodb', region_name='us-west-1').Table('menu')
        return responseBody[operation](respond(None, operations[operation](dynamo, payload)))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
