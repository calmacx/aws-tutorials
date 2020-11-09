### Prerequists
* An `aws` free account
* `aws` cli installed and configured


### Create permisions

First, create a new trust policy in `json` format:

```
$ cat trust-policy.json 
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### Upload the trust policy

There are other examples of how to do this in [these aws support documents](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-awscli.html).

Using the command line, the `json` policy can be uploaded and will give you an output something like this:
```
$ aws iam create-role --role-name lambda-ex --assume-role-policy-document file://trust-policy.json
{
    "Role": {
        "Path": "/",
        "RoleName": "lambda-ex",
        "RoleId": "AROA3GBENLBA5W3OEPEKR",
        "Arn": "arn:aws:iam::768875518017:role/lambda-ex",
        "CreateDate": "2020-11-09T12:55:32+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
    }
}
```


### Create a python function 

Create a new function that will be a lambda, and save it as `lambda_function.py`:
```
import json
def lambda_handler(event, context):
    msg = "%s %s : %s"%(event['text1'],event['text2'],event['text3'])
    return {
        'statusCode': 200,
        'body': json.dumps(msg)
    }
```

### Zip the function

To upload to AWS::Lambda, the function needs to be placed in a deployment `.zip` file:
```
zip my-deployment-package.zip lambda_function.py
```
Obviously more files with more complex functionality can be deployed like this. [These docs](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html) show how additional requirements can be added to create a package.


### Create a new AWS::Lambda function

```
$ aws lambda create-function --function-name test-message --zip-file fileb://my-deployment-package.zip --runtime python3.8 --role arn:aws:iam::768875518017:role/lambda-ex --handler lambda_function.lambda_handler
{
    "FunctionName": "test-message",
    "FunctionArn": "arn:aws:lambda:eu-west-2:768875518017:function:test-message",
    "Runtime": "python3.8",
    "Role": "arn:aws:iam::768875518017:role/lambda-ex",
    "Handler": "lambda_function.lambda_handler",
    "CodeSize": 327,
    "Description": "",
    "Timeout": 3,
    "MemorySize": 128,
    "LastModified": "2020-11-09T13:04:46.867+0000",
    "CodeSha256": "a4mwsNGL5ib6f+c355TzY7MmaxgzukXg2djMBXXZQA0=",
    "Version": "$LATEST",
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "a520f814-7772-4534-b5cd-4707f3a286d9",
    "State": "Active",
    "LastUpdateStatus": "Successful"
}
```

* Handler
   * `<name_of_file>.<name_of_function>`
   * We defined `def lambda_handler` in `lambda_function.py`, therefore in this scenario the name is `lambda_function.lambda_handler`
* Role
   * From step X.Y `arn:aws:iam::768875518017:role/lambda-ex` 



### Create an input to parse

As described, the handler is expecting to receive three variables, which it is going to format and return to us.
We can defined what these variables are in another `json` file that will be sent to the lambda function:
```
$ cat message.json 
{
      "text1":"ey",
      "text2":"up",
      "text3":"just said hello"
}
```

### Run the lambda function

Using `invoke` the function can be executed, sending the `message.json` file, and returning the output into `response.json`:
```
$ aws lambda invoke --function-name test-message --payload fileb://message.json response.json
```
Checking the response, we will see that it succeeded!
```
$ cat response.json 
{"statusCode": 200, "body": "\"ey up : just said hello\""}
```