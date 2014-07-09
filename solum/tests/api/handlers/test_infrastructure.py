# Copyright 2014 - Numergy
#
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

import mock

from solum.api.handlers import infrastructure_handler as infra
from solum.tests import base
from solum.tests import fakes
from solum.tests import utils


@mock.patch('solum.objects.registry')
class TestInfrastructureStackHandler(base.BaseTestCase):

    def setUp(self):
        super(TestInfrastructureStackHandler, self).setUp()
        self.ctx = utils.dummy_context()

    def test_get(self, mock_registry):
        mock_registry.InfrastructureStack.get_by_uuid.return_value = {}
        handler = infra.InfrastructureStackHandler(self.ctx)
        res = handler.get('test_id')
        self.assertIsNotNone(res)
        mock_registry.InfrastructureStack.get_by_uuid.assert_called_once_with(
            self.ctx, 'test_id')

    def test_get_all(self, mock_registry):
        mock_registry.StackList.get_all.return_value = {}
        handler = infra.InfrastructureStackHandler(self.ctx)
        res = handler.get_all()
        self.assertIsNotNone(res)
        mock_registry.InfrastructureStackList.get_all.assert_called_once_with(
            self.ctx)

    def test_update(self, mock_registry):
        data = {'user_id': 'new_user_id',
                'image_id': 'new_image_id',
                'heat_stack_id': 'new_stack_id'}
        db_obj = fakes.FakeInfrastructureStack()
        mock_registry.InfrastructureStack.get_by_uuid.return_value = db_obj
        handler = infra.InfrastructureStackHandler(self.ctx)
        res = handler.update('test_id', data)
        self.assertEqual(db_obj.user_id, res.user_id)
        db_obj.save.assert_called_once_with(self.ctx)
        db_obj.update.assert_called_once_with(data)
        mock_registry.InfrastructureStack.get_by_uuid.assert_called_once_with(
            self.ctx, 'test_id')

    def test_create(self, mock_registry):
        data = {'user_id': 'new_user_id',
                'image_id': 'new_image_id',
                'heat_stack_id': 'new_stack_id'}
        db_obj = fakes.FakeInfrastructureStack()
        mock_registry.InfrastructureStack.return_value = db_obj
        handler = infra.InfrastructureStackHandler(self.ctx)
        res = handler.create(data)
        db_obj.update.assert_called_once_with(data)
        db_obj.create.assert_called_once_with(self.ctx)
        self.assertEqual(db_obj, res)

    def test_delete(self, mock_registry):
        db_obj = fakes.FakeInfrastructureStack()
        mock_registry.InfrastructureStack.get_by_uuid.return_value = db_obj
        handler = infra.InfrastructureStackHandler(self.ctx)
        handler.delete('test_id')
        db_obj.destroy.assert_called_once_with(self.ctx)
        mock_registry.InfrastructureStack.get_by_uuid.assert_called_once_with(
            self.ctx, 'test_id')