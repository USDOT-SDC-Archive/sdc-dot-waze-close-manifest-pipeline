import boto3
import json
import os
from common.logger_utility import *
from common.constants import *

sqs = boto3.resource('sqs', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')


class ClosePipeline:

    def publish_message_to_sns(self, message):
        """
        Publishes a message to Amazon's Simple Notification Service
        :param message: dict
        """
        response = sns.publish(
            TargetArn=os.environ['BATCH_NOTIFICATION_SNS'],
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )

    def put_message_sqs(self, batch_id, sqs_persist):
        """
        Puts a batch into a queue via Amazon's Simple Queue Service
        :param batch_id: the batch id of the batch
        :param sqs_persist: the name of the queue
        :return:
        """
        try:
            queue = sqs.get_queue_by_name(QueueName=sqs_persist)
            response = queue.send_message(MessageBody=json.dumps({
                'BatchId': batch_id
            }))

            LoggerUtility.logInfo(
                "Successfully put message to persist sqs for batch id - {}, response - {}".format(batch_id, response))
        except Exception as e:
            LoggerUtility.logError(
                "Unable to put message to persist sqs for batch id - {} , sqs - {}".format(batch_id, sqs_persist))
            raise e

    def delete_sqs_message(self, event, context):
        """
        Moves a message to the persistence queue, then deletes it from the previous queue via Amazon's Simple Queue
        Service.
        :param event: a list with a dictionary that contains information on a batch(?) # might be nice to put down the
            structure of the dictionary
            - Is the event a single item list?
        :param context: idk but it's not used
        :return:
        """
        batchId = ""  # are batch ids strings or ints
        try:
            if "queueUrl" in event[0]:
                queueUrl = event[0]["queueUrl"]
                receiptHandle = event[0]["receiptHandle"]
                batchId = event[0]["batch_id"]
                is_historical = event[0]["is_historical"] == "true"
                persistenceQueue = os.environ['SQS_PERSIST_ARN']
                if is_historical:
                    persistenceQueue = os.environ['SQS_PERSIST_HISTORICAL_ARN']

                # put the message into the persistence queue via batchId
                self.put_message_sqs(batchId, persistenceQueue)
                txt = json.dumps(event[0])

                # delete message from the previous queue.
                if json.loads(txt).get("queueUrl") is not None:
                    message = sqs.Message(queueUrl, receiptHandle)
                    message.delete()
                    LoggerUtility.logInfo("Message deleted from sqs for batchId {}".format(batchId))
                    self.publish_message_to_sns({"BatchId": batchId, "Status": "Manifest generation completed"})
        except Exception as e:
            LoggerUtility.logError("Unable to delete sqs message for batchId {}".format(batchId))
            raise e
    
    def close_pipeline(self, event, context):
        """
        Executes delete_sqs_message
        :param event:
        :param context:
        :return:
        """
        self.delete_sqs_message(event, context)
