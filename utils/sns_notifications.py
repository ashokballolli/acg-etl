import boto3

snsARN = 'arn:aws:sns:eu-central-1:212577831031:sns-acg-etl'
def notify(text):
    try:
        sns = boto3.client('sns')
        sns.publish(TopicArn = snsARN, Message = text)
    except Exception as e:
        print("Not able to send SMS due to {}".format(e))
        exit(1)


notify("Database connection failed due to")