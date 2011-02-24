# Copyright 2011 OpenStack, LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
This module provides SchedulerDependentManager, a base class for
any Manager that has Capabilities that should be related to the
Scheduler.

These Capabilities are hints that can help the scheduler route
requests to the appropriate service instance.
"""

import sys

from nova import flags
from nova import manager
from nova.scheduler import api
from nova import log as logging


FLAGS = flags.FLAGS


class SchedulerDependentManager(manager.Manager):

    """Periodically send capability updates to the Scheduler services.
       Services that need to update the Scheduler of their capabilities
       should derive from this class. Otherwise they can derive from
       manager.Manager directly. Updates are only sent after
       update_service_capabilities is called with non-None values."""

    def __init__(self, host=None, db_driver=None, service_name="undefined"):
        self.last_capabilities = None
        self.service_name = service_name
        super(SchedulerDependentManager, self).__init__(host, db_driver)

    def update_service_capabilities(self, capabilities):
        """Remember these capabilities to send on next periodic update."""
        self.last_capabilities = capabilities

    def periodic_tasks(self, context=None):
        """Pass data back to the scheduler at a periodic interval"""
        if self.last_capabilities:
            logging.debug(_("*** Notifying Schedulers of capabilities ..."))
            api.API.update_service_capabilities(context, self.service_name,
                                self.last_capabilities)

        super(SchedulerDependentManager, self).periodic_tasks(context)
