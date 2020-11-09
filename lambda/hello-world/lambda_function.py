import json
def lambda_handler(event, context):
    msg = "%s %s : %s"%(event['text1'],event['text2'],event['text3'])
    return {
        'statusCode': 200,
        'body': json.dumps(msg)
    }
