import unittest
import json
from app import Request_Body, generate_quarter_offsets, validate_input, lambda_handler

class AppTests(unittest.TestCase):

    def test_parse_body(self):
        stringified_event = json.dumps({
            "body": '{ "start_year": 2023, "start_quarter": 1, "end_year": 2023, "end_quarter": 2 }'
        })

        event = json.loads(stringified_event)
        body: Request_Body = json.loads(event['body'])

        s_year = body['start_year']
        s_quarter = body['start_quarter']
        e_year = body['end_year']
        e_quarter = body['end_quarter']

        self.assertEqual(s_year, 2023, 'start year is correct')
        self.assertEqual(s_quarter, 1, 'start quarter is correct')
        self.assertEqual(e_year, 2023, 'end year is correct')
        self.assertEqual(e_quarter, 2, 'end quarter is correct')

    def test_validate_input_start_before_end(self):
        s_year = 2023
        s_quarter = 4
        e_year = 2023
        e_quarter = 3

        expeceted_is_valid = validate_input(s_year, s_quarter, e_year, e_quarter)

        self.assertEqual(expeceted_is_valid, False, "Should return false when start date is after end date.")
    
    def test_validate_input_with_too_big_quarter(self):
        s_year = 2023
        s_quarter = 6
        e_year = 2023
        e_quarter = 3

        expeceted_is_valid = validate_input(s_year, s_quarter, e_year, e_quarter)

        self.assertEqual(expeceted_is_valid, False, "Should return false when quarter is > 4")

    def test_validate_input_with_too_small_quarter(self):
        s_year = 2023
        s_quarter = 0
        e_year = 2023
        e_quarter = 3

        expeceted_is_valid = validate_input(s_year, s_quarter, e_year, e_quarter)

        self.assertEqual(expeceted_is_valid, False, "Should return false when quarter is < 1")

    def test_validate_input_with_valid(self):
        s_year = 2023
        s_quarter = 1
        e_year = 2023
        e_quarter = 4

        expeceted_is_valid = validate_input(s_year, s_quarter, e_year, e_quarter)

        self.assertEqual(expeceted_is_valid, True, "Should be valid")

    def test_generate_quarter_offsets_with_one(self):
        # this test is made to work in quarter 3, 2023
        s_year = 2023
        s_quarter = 3
        e_year = 2023
        e_quarter = 3

        expected = generate_quarter_offsets(s_year, s_quarter, e_year, e_quarter)

        self.assertEqual(expected, [0], "There should be one value. It should be 0 because the offset is today - today. ")

    def test_generate_quarter_offsets_with_mulitple(self):
        # this test is made to work in quarter 3, 2023
        s_year = 2020
        s_quarter = 1
        e_year = 2023
        e_quarter = 3

        expected = generate_quarter_offsets(s_year, s_quarter, e_year, e_quarter)

        self.assertEqual(expected, [-14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0], "There should be 15 quarters between start and end.")
    

    def test_lambda_handler_with_invalid_input(self):
        # this test is made to work in quarter 3, 2023
        stringified_event = json.dumps({
            "body": '{ "start_year": 2023, "start_quarter": 0, "end_year": 2023, "end_quarter": 2 }'
        })

        event = json.loads(stringified_event)

        expected = {
            'statusCode': 400,
            'body': json.dumps({'message': 'invalid input'})
        }

        actual = lambda_handler(event, '')

        self.assertEqual(expected, actual, "Should return 400 when invalid input.")
        

if __name__ == '__main__':
    unittest.main()