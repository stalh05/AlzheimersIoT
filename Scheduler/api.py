from flask import Flask
from flask_restful import Resource, Api, reqparse
from MessageScheduler import MessageScheduler

app = Flask(__name__)
api = Api(app)


class Scheduler(Resource):
    __message_scheduler = MessageScheduler()

    def get(self):
        return {'message': 'You\'ve sent a GET request to the Scheduler API'}

    def post(self):
        try:
            # Parse the args
            args = self.__get_parsed_args()

            # Check that the medium is supported
            self.__check_medium_is_supported(args['medium'])

            # Check for valid time
            # TODO: write a helper function

            # Send to the Scheduler
            self.__message_scheduler.add_message(args)

            return {'Created a job with the args:' : args}

        except Exception as e:
            return {'error': str(e)}

    def __get_parsed_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument('medium', type=str,
                            help='Medium to send the msg over, e.g. \'SMS\', \'Email\', \'Google Home\')')
        parser.add_argument('time', type=str, help='Execution time in format \'YYYY-MM-DD HH:MM:SS +0000\'')
        parser.add_argument('dest', type=str, help='Destination, e.g. \'123-456-789\', \'example@domain.com\'')
        parser.add_argument('msg', type=str, help='The message to send')

        return parser.parse_args()

    def __check_medium_is_supported(self, medium):
        supported_mediums = ['SMS', 'Email', 'Google Home']
        if medium not in supported_mediums:
            raise Exception("Medium {} is not supported.".format(medium))


api.add_resource(Scheduler, '/api/scheduler')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


# Example body of a POST request
# args = {
#     'medium': 'SMS',
#     'time': '2017-03-27 23:58:00',
#     'dest': '123-456-7890',
#     'msg': 'hello'
# }