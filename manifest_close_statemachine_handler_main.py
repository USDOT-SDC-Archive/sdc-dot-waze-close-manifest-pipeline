from common.logger_utility import LoggerUtility
from lambdas.manifest_close_statemachine_handler import ClosePipeline


def lambda_handler(event, context):
    LoggerUtility.set_level()
    close_pipeline_handle_event = ClosePipeline()
    close_pipeline_handle_event.close_pipeline(event)
    return event
