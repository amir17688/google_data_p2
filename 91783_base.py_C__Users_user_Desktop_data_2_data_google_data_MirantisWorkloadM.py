# Copyright 2016 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import abc

from oslo_utils import reflection
from taskflow import retry
from taskflow import task
from taskflow.patterns import linear_flow

from cloudferry.lib.os.discovery import model
from cloudferry.lib.utils import taskflow_utils
from cloudferry.lib.utils import utils


class MigrationFlowFactory(object):
    """
    Base class for migration task flow factories. Class deriving from
    MigrationFlowFactory should define ``migrated_class`` class attribute
    which should be assigned to model class the factory will create migration
    flows for and ``create_flow`` method that should return list of task
    objects.

    Example::

        class TenantMigrationFlowFactory(base.MigrationFlowFactory):
            migrated_class = keystone.Tenant

            def create_flow(self, config, migration, obj):
                return [
                    CreateTenant(obj, config, migration),
                    base.RememberMigration(obj),
                ]
    """

    __metaclass__ = abc.ABCMeta

    migrated_class = None

    @abc.abstractmethod
    def create_flow(self, config, migration, obj):
        """
        Implementing methods should return list of TaskFlow task objects.
        :param config: cloudferry configuration
        :param migration: migration configuration
        :param obj: object to migrate
        :return: list of taskflow.task.Task instances
        """
        return []


class ObjectTask(task.Task):
    """
    Base class for object migration tasks that make it easier to write object
    migration tasks by skipping serialization/deserialization of model.Model
    instances.

    Instead of implementing ``execute`` method, tasks deriving from this class
    should implement migrate method.
    """

    def __init__(self, obj, **kwargs):
        super(ObjectTask, self).__init__(
            name='{0}_{1}'.format(utils.qualname(self.__class__),
                                  taskflow_utils.object_name(obj)),
            requires=reflection.get_callable_args(self.migrate),
            **kwargs)
        self.src_object = obj

    @abc.abstractmethod
    def migrate(self, *args, **kwargs):
        """
        Perform any operations necessary for migration and return any objects
        that the task should provide.
        """
        pass

    def execute(self, *args, **kwargs):
        result = self.migrate(
            *[self._deserialize(arg) for arg in args],
            **{key: self._deserialize(value)
               for key, value in kwargs.items()})
        if result is not None:
            return [self._serialize(val) for val in result]

    @staticmethod
    def _serialize(obj):
        if not isinstance(obj, model.Model):
            return obj
        return {
            'type': obj.get_class_qualname(),
            'object': obj.dump(),
        }

    @staticmethod
    def _deserialize(obj_dict):
        if not isinstance(obj_dict, dict):
            return obj_dict
        if 'type' not in obj_dict:
            return obj_dict
        try:
            model_cls = model.get_model(obj_dict['type'])
        except ImportError:
            return obj_dict
        if not issubclass(model_cls, model.Model):
            return obj_dict
        return model_cls.load(obj_dict['object'])


class RememberMigration(ObjectTask):
    """
    Task that will store migrated object on destination cloud to local database
    and save link between original and destination object.
    """

    def __init__(self, src_object):
        super(RememberMigration, self).__init__(src_object)

    def migrate(self, dst_object, *args, **kwargs):
        with model.Session() as session:
            self.src_object.link_to(dst_object)
            session.store(dst_object)
            session.store(self.src_object)


def create_migration_flow(obj, config, migration):
    """
    Creates migration flow for object ``obj`` based on configuration ``config``
    migration ``migration``.
    :param obj: model.Model instance
    :param config: configuration
    :param migration: migration (part of configuration)
    :return: migration flow for an object
    """

    if obj.find_link(migration.destination) is not None:
        return None
    cls = obj.get_class()
    flow_factories = migration.migration_flow_factories
    if cls not in flow_factories:
        raise RuntimeError('Failed to find migration flow factory')
    else:
        flow = linear_flow.Flow('top_level_' + taskflow_utils.object_name(obj),
                                retry=retry.AlwaysRevert())
        factory = flow_factories[cls]()
        migration_tasks = factory.create_flow(config, migration, obj)
        flow.add(*migration_tasks)
        return flow
