import boto3
import os
from os import environ
import sys
from utils.log_utils import setup_logging
import yaml
import logging
from datetime import datetime

CONFIG_FILE = os.path.join(sys.path[0], './resources/config.yml')
setup_logging(CONFIG_FILE)

sns = yaml.load(open(CONFIG_FILE), Loader=yaml.BaseLoader)['sns']
sns_arn = environ.get('sns_arn') or sns['arn']
send_notification = eval(environ.get('send_notification')) or eval(sns['send_notification'])

def send_sns_message(subject, message):
    try:
        sns = boto3.client('sns')
        response = sns.publish(TopicArn = sns_arn,
                    Subject = subject,
                    Message = message)
        logging.debug("SNS response: {}".format(response['ResponseMetadata']['HTTPStatusCode']))
    except Exception as ex:
        logging.error("Error Sending SNS message {}".format(ex))
        exit(1)

def build_message(is_success, message):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

    if is_success:
        subject = "[ACG-ETL] Job has completed - {}".format(dt_string)
        message = """
        Hi,
        COVID daily stats refreshed with {} rows
        
        Thanks & Regards,
        ACG-Etl
        """.format(message)
    else:
        subject = "[ACG-ETL] Error during the table refresh - {}".format(dt_string)
        message = """
        Hi,
        There was error during the covid data refresh.
        Error message: {}
        
        Thanks & Regards,
        ACG-Etl
        """.format(message)
    return subject, message

def notify_etl_status(is_success, message):

    if send_notification:
        subject, message = build_message(is_success, message)
        send_sns_message(subject, message)