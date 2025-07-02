from flask_restful import Resource, reqparse
from app.controllers.submission_process import (
    main_process
)
from app.helpers.response_reapper import response_wrapper
from flask import request


parser = reqparse.RequestParser()

class SubmissionProcess(Resource):
    def post(self):
        try:
            json_raw = request.get_json(silent=True)
            data = json_raw.get('products')
            user_input = json_raw.get('user-input')
            weights = json_raw.get('weights')

            return main_process(data, weights, user_input)
            # return raw_json_data
        except Exception as e:
            return {"message": f"Terjadi kesalahan: {str(e)}"}, 500
        
def register_api_routes(api):
    api.add_resource(SubmissionProcess, "/api/submission/process")