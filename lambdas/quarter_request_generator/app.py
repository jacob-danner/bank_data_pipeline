import json
from dateutil.relativedelta import relativedelta
from datetime import date
import math
import os
import boto3

from typing import TypedDict

'''
HELPER FUNCTIONS
'''
quarter_to_month_map = {
    1: '01',
    2: '04',
    3: '07',
    4: '10',
}

def validate_input(s_year, s_quarter, e_year, e_quarter):
    if s_quarter not in quarter_to_month_map:
        return False
    if e_quarter not in quarter_to_month_map:
        return False

    start_date = date.fromisoformat(f'{s_year}-{quarter_to_month_map[s_quarter]}-01')
    end_date = date.fromisoformat(f'{e_year}-{quarter_to_month_map[e_quarter]}-01')

    if start_date > end_date:
        return False

    return True


def generate_quarter_offsets(s_year, s_quarter, e_year, e_quarter):

    start_date = date.fromisoformat(f'{s_year}-{quarter_to_month_map[s_quarter]}-01')
    end_date = date.fromisoformat(f'{e_year}-{quarter_to_month_map[e_quarter]}-01')

    today = date.today()
    todays_quarter = math.ceil(date.today().month / 3)
    current_quarter_date = date.fromisoformat(f'{today.year}-{quarter_to_month_map[todays_quarter]}-01')

    quarter_offsets = []
    date_iterator = start_date
    while (date_iterator) <= end_date:
        # calculate the negative offset of quarters from currentquarer
        num_months_between = (current_quarter_date.year - date_iterator.year) * 12 + current_quarter_date.month - date_iterator.month
        num_quarters_between = num_months_between // 3
        cur_quarter_offset = -num_quarters_between

        quarter_offsets.append(cur_quarter_offset)
        date_iterator += relativedelta(months=+3)

    return quarter_offsets
    
    
    
'''
HANDLER LOGIC
'''

class Request_Body(TypedDict):
    start_year: int
    start_quarter: int
    end_year: int
    end_quarter: int
    
# for testing. invoke from api gateway with this as the body
# {
#     "start_year": 2023,
#     "start_quarter": 1,
#     "end_year": 2023,
#     "end_quarter": 3
# }


def lambda_handler(event, context):
    print(f'event: {event}')
    
    body: Request_Body = json.loads(event['body'])
    print(f'body: {body}')

    QUARTER_DATA_COLLECTOR_ARN = os.environ['QUARTER_DATA_COLLECTOR_ARN']
    print(f'QUARTER_DATA_COLLECTOR_ARN: {QUARTER_DATA_COLLECTOR_ARN}')

    s_year = body['start_year']
    s_quarter = body['start_quarter']
    e_year = body['end_year']
    e_quarter = body['end_quarter']

    print(f's_year: {s_year}. s_quarter: {s_quarter}')
    print(f'e_year: {e_year}. e_quarter: {e_quarter}')

    is_valid = validate_input(s_year, s_quarter, e_year, e_quarter)
    
    if not is_valid:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'invalid input'})
        }

    quarter_offsets = generate_quarter_offsets(s_year, s_quarter, e_year, e_quarter)

    # send requests to quarter_data_collector lambdas
    client = boto3.client('lambda')
    for q_offset in quarter_offsets:
        response = client.invoke(FunctionName=QUARTER_DATA_COLLECTOR_ARN)
        
        print(response)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'successfully triggered quarter_data_collector lambdas'})
    }