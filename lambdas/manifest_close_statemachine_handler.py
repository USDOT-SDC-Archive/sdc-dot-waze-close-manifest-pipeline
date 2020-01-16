import json
import os

import boto3

from common.logger_utility import LoggerUtility


class ClosePipeline:

    sqs = boto3.resource('sqs', region_name='us-east-1')
    sns = boto3.client('sns', region_name='us-east-1')
    LoggerUtility.log_info("Test test 123")

    def publish_message_to_sns(self, message):
        """
        Publishes a message to Amazon's Simple Notification Service
        :param message: dict
        """
        self.sns.publish(
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
            queue = self.sqs.get_queue_by_name(QueueName=sqs_persist)
            response = queue.send_message(MessageBody=json.dumps({
                'BatchId': batch_id
            }))

            LoggerUtility.log_info(
                "Successfully put message to persist sqs for batch id - {}, response - {}".format(batch_id, response))
        except Exception as e:
            LoggerUtility.log_error(
                "Unable to put message to persist sqs for batch id - {} , sqs - {}".format(batch_id, sqs_persist))
            raise e

    def delete_sqs_message(self, event, context):
        """
        Moves a message to the persistence queue, then deletes it from the previous queue via Amazon's Simple Queue
        Service.
        :param event: a list with a dictionary that contains information on a batch
        :param context: not used.  Logging it
        :return:
        """
        LoggerUtility.log_info("context: {}".format(context))
        batch_id = ""
        try:
            if "queueUrl" in event[0]:
                queue_url = event[0]["queueUrl"]
                receipt_handle = event[0]["receiptHandle"]
                batch_id = event[0]["batch_id"]
                is_historical = event[0]["is_historical"] == "true"

                persistence_queue = os.environ['SQS_PERSIST_ARN']
                if is_historical:
                    persistence_queue = os.environ['SQS_PERSIST_HISTORICAL_ARN']

                # put the message into the persistence queue via batchId
                self.put_message_sqs(batch_id, persistence_queue)
                txt = json.dumps(event[0])

                # delete message from the previous queue.
                if json.loads(txt).get("queueUrl") is not None:
                    message = self.sqs.Message(queue_url, receipt_handle)
                    message.delete()
                    LoggerUtility.log_info("Message deleted from sqs for batchId {}".format(batch_id))
                    self.publish_message_to_sns({"BatchId": batch_id, "Status": "Manifest generation completed"})
        except Exception as e:
            LoggerUtility.log_error("Unable to delete sqs message for batchId {}".format(batch_id))
            raise e

    def close_pipeline(self, event, context):
        """
        Executes delete_sqs_message
        :param event: a list with a dictionary that contains information on a batch
        :param context: not used.  Just passed to
        :return:
        """
        self.delete_sqs_message(event, context)
