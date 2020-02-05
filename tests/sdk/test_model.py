import json
import unittest

import requests
import requests_mock

from hydrosdk.sdk import Model, Signature, Application, Monitoring

DEV_ENDPOINT = "http://localhost"

PATH_TO_MODEL = ""


class ModelSpec(unittest.TestCase):
    def test_model_creation(self):
        monitoring = [
            Monitoring('test').with_health(True).with_spec('LatencyMetricSpec', interval=15),
            Monitoring('acc').with_health(True).with_spec("Accuracy")
        ]
        res = [x.compile() for x in monitoring]
        print(res)

        signature = Signature('infer') \
            .with_input('in1', 'double', [-1, 2], 'numerical') \
            .with_output('out1', 'double', [-1], 'numerical')


        model = Model() \
            .with_name("sdk-model") \
            .with_runtime("hydrosphere/serving-runtime-python-3.6:dev") \
            .with_payload([PATH_TO_MODEL]) \
            .with_monitoring(monitoring) \
            .with_signature(signature)
        print(model)
        model.compile()
        print(model.inner_model.__dict__)


    def test_model_apply(self):
        # monitoring = [
        #     Monitoring('test').with_health(True).with_spec('LatencyMetricSpec', interval=15),
        #     Monitoring('acc').with_health(True).with_spec("Accuracy")
        # ]
        signature = Signature().with_name('infer') \
            .with_input('in1', 'double', [-1, 2], 'numerical') \
            .with_output('out1', 'double', [-1], 'numerical')
        model = Model() \
            .with_name("sdk-model") \
            .with_runtime("hydrosphere/serving-runtime-python-3.6:dev") \
            .with_payload([PATH_TO_MODEL]) \
            .with_signature(signature) \
            # .with_monitoring(monitoring)
        result = model.apply(DEV_ENDPOINT)
        print(model.inner_model.__dict__)
        print(result)

    def test_singular_application_apply(self):
        # def matcher(req):
        #     print(req.text)
        #     resp = requests.Response()
        #     resp.status_code = 200
        #     resp._content = json.dumps({'id': 1}).encode("utf-8")
        #     return resp
        # with requests_mock.Mocker() as mock:
        #     mock.add_matcher(matcher)
        # monitoring = [
        #     Monitoring('sdk-ae') \
        #         .modelversion("autoencoder:10") \
        #         .threshold(threshold=10, threshold_cmp="<=")
        # ]
        signature = Signature().with_name('infer') \
            .with_input('in1', 'double', [-1, 2], 'numerical') \
            .with_output('out1', 'double', [-1], 'numerical')

        model = Model() \
            .with_name("sdk-model") \
            .with_runtime("hydrosphere/serving-runtime-python-3.6:dev") \
            .with_payload([PATH_TO_MODEL]) \
            .with_signature(signature) \
            # .with_monitoring(monitoring)

        app = Application.singular("sdk-app", model)
        result = app.apply(DEV_ENDPOINT)
        print(app.compiled)
        print(result)

