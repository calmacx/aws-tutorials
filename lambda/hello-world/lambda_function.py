import json
def lambda_handler(event, context):
    x = event['x']
    y = event['y']
    msg = event['msg']
    return {
        'statusCode': 200,
        'msg': json.dumps(msg.lower()),
        'product': x*y,
        'diff': x-y
    }
