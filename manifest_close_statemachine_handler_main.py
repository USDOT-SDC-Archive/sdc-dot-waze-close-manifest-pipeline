from lambdas.persistence_close_statemachine_handler import *
from common.logger_utility import *
from common.constants import *

def lambda_handler(event, context):
    LoggerUtility.setLevel()
    close_pipeline_handle_event = ClosePipeline()
    close_pipeline_handle_event.close_pipeline(event, context)
    return event