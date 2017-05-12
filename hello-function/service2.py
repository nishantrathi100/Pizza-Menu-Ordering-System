from __future__ import print_function

import json
import boto3
import time

print('Loading function')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def updateOrder1(order, odr):
    bod={}
    Key={}
    ExpressionAttributeNames={}
    ExpressionAttributeValues = {}
    Key["order_id"]=order["order_id"]
    ExpressionAttributeNames["#ODR"]="order"
    ExpressionAttributeValues[":SELV"]={"selection":odr["selection"]}
    UpdateExpression = 'SET #ODR = :SELV'
    bod["Key"] = Key
    bod["ExpressionAttributeNames"]=ExpressionAttributeNames
    bod["ExpressionAttributeValues"]=ExpressionAttributeValues
    bod["TableName"]="order"
    bod["UpdateExpression"]=UpdateExpression
    return bod

def updateOrder2(order, odr):
    bod={}
    Key={}
    ExpressionAttributeNames={}
    ExpressionAttributeValues = {}
    Key["order_id"]=order["order_id"]
    ExpressionAttributeNames["#ODR"]="order"
    ExpressionAttributeNames["#ODR2"]="order_status"
    ExpressionAttributeValues[":VAL"]={"selection":odr["selection"],"costs":odr["costs"],"size":odr["size"],"order_time":odr["order_time"]}
    ExpressionAttributeValues[":VAL2"]="processing"
    UpdateExpression = 'SET #ODR = :VAL, #ODR2 = :VAL2'
    bod["Key"] = Key
    bod["ExpressionAttributeNames"]=ExpressionAttributeNames
    bod["ExpressionAttributeValues"]=ExpressionAttributeValues
    bod["TableName"]="order"
    bod["UpdateExpression"]=UpdateExpression
    return bod

def getMenu(menu_id):
    x={}
    x["Key"]={"menu_id":menu_id}
    dynamo = boto3.resource('dynamodb', region_name='us-west-1').Table('menu')
    menu = respond(None, dynamo.get_item(**x))
    return menu

def getOrder(payload):
    x={}
    

def postResponseHandler(x, payload):
    menu=getMenu(payload["Item"]["menu_id"])
    bod={}
    bod["Message"] = "Hi "+payload["Item"]["customer_name"]+", please choose one of these selection: "
    i = 1
    putComma = False
    for sel in menu["body"]["Item"]["selection"]:
        if (putComma):
            bod["Message"] = bod["Message"] + ","
        bod["Message"] = bod["Message"] + " " + str(i) + ". " + sel
        putComma = True
        i = i + 1
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
        'GET': lambda dynamo, x: dynamo.get_item(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }

    responseBody = {
        'DELETE': lambda x: "200 OK" if x["statusCode"] == "200" else"ERROR" ,
        'GET': lambda x: x["body"]["Item"],
        'POST': lambda x, payload: postResponseHandler(x, payload) if x["statusCode"] == "200" else"ERROR" ,
        'PUT': lambda x: "200 OK" if x["statusCode"] == "200" else"ERROR" ,
    }

    operation = event['httpMethod']
    if operation == "POST":
        payload = event['body']
        dynamo = boto3.resource('dynamodb', region_name='us-west-1').Table('order')
        return responseBody[operation](respond(None, operations[operation](dynamo, payload)),payload)
    if operation == "PUT":
        inputChoice = event['input']
        order_id = event['order_id']
        x={}
        x["Key"]={"order_id":order_id}
        dynamo = boto3.resource('dynamodb', region_name='us-west-1').Table('order')
        order = respond(None, operations["GET"](dynamo, x))["body"]["Item"]
        menu = getMenu(order["menu_id"])
        if "order" in order:
            if "costs" in order["order"]:
                return {"Message":"Your order has been already placed!"}
            else:
                odr = {}
                inp = int(inputChoice)
                inp = inp - 1
                odr["size"] = menu["body"]["Item"]["size"][inp]
                odr["costs"] = menu["body"]["Item"]["price"][inp]
                odr["order_time"] = time.strftime("%m-%d-%Y@%H:%M:%S")
                odr["selection"]=order["order"]["selection"]
                bod = updateOrder2(order, odr)
                #update the db
                response2 = respond(None, operations[operation](dynamo, bod))
                if response2["statusCode"] == "200":
                    msg={}
                    msg["Message"]="Your order costs $"+ str(float(menu["body"]["Item"]["price"][inp])) +". We will email you when the order is ready. Thank you!";
                    return msg
        else:
            odr = {}
            inp = int(inputChoice)
            inp = inp - 1
            odr["selection"] = menu["body"]["Item"]["selection"][inp]
            bod = updateOrder1(order, odr)
            print('1111')
            print(bod)
            response1 = respond(None, operations[operation](dynamo, bod))
            if response1["statusCode"] == "200":
                bod2={}
                bod2["Message"] = "Which size do you want?"
                i = 1
                putComma = False
                for size in menu["body"]["Item"]["size"]:
                    if (putComma):
                        bod2["Message"] = bod2["Message"] + ","
                    bod2["Message"] = bod2["Message"] + " " + str(i) + ". " + size
                    putComma = True
                    i = i + 1
                return bod2
    if operation == "GET":
        order_id = event['order_id']
        x={}
        x["Key"]={"order_id":order_id}
        dynamo = boto3.resource('dynamodb', region_name='us-west-1').Table('order')
        return respond(None, operations["GET"](dynamo, x))["body"]["Item"]
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
