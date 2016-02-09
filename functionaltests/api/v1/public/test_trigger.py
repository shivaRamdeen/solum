# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json

import requests

from functionaltests.api import base


class TestTriggerController(base.TestCase):

    def test_trigger_post(self):
        resp = self.client.create_app()
        bdy = json.loads(resp.body)
        trigger_uri = bdy['trigger_uri']
        # Using requests instead of self.client to test unauthenticated request
        status_url = 'https://api.github.com/repos/u/r/statuses/{sha}'
        body_dict = {'sender': {'url': 'https://api.github.com'},
                     'pull_request': {'head': {'sha': 'asdf'}},
                     'repository': {'statuses_url': status_url}}
        body = json.dumps(body_dict)
        resp = requests.post(trigger_uri, data=body)
        self.assertEqual(resp.status_code, 202)

    def test_trigger_post_with_empty_body(self):
        resp = self.client.create_app()
        bdy = json.loads(resp.body)
        trigger_uri = bdy['trigger_uri']
        # Using requests instead of self.client to test unauthenticated request
        resp = requests.post(trigger_uri)
        self.assertEqual(resp.status_code, 400)
