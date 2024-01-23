echo "Creating Stack for SQS"
aws cloudformation create-stack --stack-name bunnyStackQueue --template-body file://create_sqs.yaml --parameters ParameterKey=QueueName,ParameterValue=bunnyQueue --region ap-south-1

timeout /t 6

echo "Creating Stack for SNS"
aws cloudformation create-stack --stack-name bunnyStackSns --template-body file://create_sns.yaml --parameters ParameterKey=TopicName,ParameterValue=bunnySns ParameterKey=SubscriptionProtocol,ParameterValue=sqs ParameterKey=DisplayName,ParameterValue=bunnySns --capabilities CAPABILITY_IAM --region ap-south-1

timeout /t 6

echo "Creating Stack for Lambda Using SAM"
sam deploy --template-file ./template.yaml --stack-name sam-template --confirm-changeset --capabilities CAPABILITY_IAM
