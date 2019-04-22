# file: locustfile
import locust
import random
import json


class VectorAppUserBehaviour(locust.TaskSet):

    def on_start(self):
        b = [random.random() for _ in range(1000)]
        a = [random.random() for _ in range(1000)]
        self.payloads = {
            "small": json.dumps({
                "a": a[:10],
                "b": b[:10],
                "op": "dot"
            }),
            "medium": json.dumps({
                "a": a[:100],
                "b": b[:100],
                "op": "sub"
            }),
            "large": json.dumps({
                "a": a[:1000],
                "b": b[:1000],
                "op": "add"
            })
        }

    @locust.task(1)
    def send_req_with_small_payload(self):
        self.client.post('/vector/', data=self.payloads['small'])

    @locust.task(1)
    def send_req_with_medium_payload(self):
        self.client.post('/vector/', data=self.payloads['medium'])

    @locust.task(1)
    def send_req_with_large_payload(self):
        self.client.post('/vector/', data=self.payloads['large'])


class VectorAppUser(locust.HttpLocust):

    task_set = VectorAppUserBehaviour
    min_wait = 1000
    max_wait = 2000
