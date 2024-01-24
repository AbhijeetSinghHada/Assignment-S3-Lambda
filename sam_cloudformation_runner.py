import boto3

def kms_key_generate(bucket_name, sqs_queue_name):
    client_cf = boto3.client('cloudformation')
    cf_template = open('kms_key.yaml').read()

    response = client_cf.create_stack(
        StackName='kms-key-stack',
        TemplateBody = cf_template,
        Parameters=[
            {
                'ParameterKey': 'BucketName',
                'ParameterValue': bucket_name
            },
            {
                'ParameterKey': 'SQSQueueName',
                'ParameterValue': sqs_queue_name
            }
        ],
        Capabilities=[
            'CAPABILITY_IAM',
        ],
    )
    print("Waiting for KMS Key stack to be created...")
    waiter = client_cf.get_waiter('stack_create_complete')
    waiter.wait(
        StackName='kms-key-stack'
    )
    print(response)
    return response

def create_s3_bucket(bucket_name):
    client_cf = boto3.client('cloudformation')
    cf_template = open('s3_logs_bucket.yaml').read()

    response = client_cf.create_stack(
        StackName='s3-bucket-stack',
        TemplateBody = cf_template,
        Parameters=[
            {
                'ParameterKey': 'BucketName',
                'ParameterValue': bucket_name
            }
        ],
        Capabilities=[
            'CAPABILITY_IAM',
        ],
    )
    print("Waiting for S3 Bucket stack to be created...")
    waiter = client_cf.get_waiter('stack_create_complete')
    waiter.wait(
        StackName='s3-bucket-stack'
    )
    print(response)
    return response

def create_sqs_queue(sqs_queue_name):
    client_cf = boto3.client('cloudformation')
    cf_template = open('create_sqs.yaml').read()

    response = client_cf.create_stack(
        StackName='sqs-queue-stack',
        TemplateBody = cf_template,
        Parameters=[
            {
                'ParameterKey': 'QueueName',
                'ParameterValue': sqs_queue_name
            }
        ],
        Capabilities=[
            'CAPABILITY_IAM',
        ],
    )
    print("Waiting for SQS Queue stack to be created...")
    waiter = client_cf.get_waiter('stack_create_complete')
    waiter.wait(
        StackName='sqs-queue-stack'
    )
    print(response)
    return response

def create_sns_topic(sns_topic_name, sns_topic_display_name):
    client_cf = boto3.client('cloudformation')
    cf_template = open('create_sns.yaml').read()

    response = client_cf.create_stack(
        StackName='sns-topic-stack',
        TemplateBody = cf_template,
        Parameters=[
            {
                'ParameterKey': 'TopicName',
                'ParameterValue': sns_topic_name
            },
            {
                'ParameterKey': 'DisplayName',
                'ParameterValue': sns_topic_display_name
            }
        ],
        Capabilities=[
            'CAPABILITY_IAM',
        ],
    )
    print("Waiting for SNS Topic stack to be created...")
    waiter = client_cf.get_waiter('stack_create_complete')
    waiter.wait(
        StackName='sns-topic-stack'
    )
    print(response)
    return response

def create_lambda_excecution_role():
    client_cf = boto3.client('cloudformation')
    cf_template = open('iam_policy.yaml').read()

    response = client_cf.create_stack(
        StackName='lambda-execution-role-stack',
        TemplateBody = cf_template,
        Capabilities=[
            'CAPABILITY_IAM',
            'CAPABILITY_NAMED_IAM'
        ],
    )
    print("Waiting for Lambda Execution Role stack to be created...")
    waiter = client_cf.get_waiter('stack_create_complete')
    waiter.wait(
        StackName='lambda-execution-role-stack'
    )
    print(response)
    return response


if __name__ == '__main__':
    bucket_name = 'sns-message-logs-2024'
    sqs_queue_name = 'mediator-queue-sns-lambda'
    kms_key_generate(bucket_name, sqs_queue_name)
    create_s3_bucket(bucket_name)
    sns_topic_name = 'sns-topic-sns-lambda'
    sns_topic_display_name = 'SNS Topic for Lambda'
    create_sqs_queue(sqs_queue_name)
    create_sns_topic(sns_topic_name, sns_topic_display_name)
    create_lambda_excecution_role()



