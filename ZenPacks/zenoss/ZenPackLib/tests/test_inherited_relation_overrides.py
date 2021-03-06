#!/usr/bin/env python

##############################################################################
#
# Copyright (C) Zenoss, Inc. 2018, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""
    This is designed to test whether or not a relation added to a 
    zenpacklib.Device subclass wipes out other relations added to 
    Products.ZenModel.Device (ZEN-24108)
"""
from ZenPacks.zenoss.ZenPackLib.tests import ZPLBaseTestCase


YAML_DOC = """
name: ZenPacks.zenoss.RelationOverrides

class_relationships:
- Products.ZenModel.Device.Device 1:MC RabbitMQAPI_Node
- RabbitMQAPI_Node 1:MC RabbitMQAPI_VHost
- RabbitMQAPI_VHost 1:MC RabbitMQAPI_Exchange
- RabbitMQAPI_VHost 1:MC RabbitMQAPI_Queue

classes:
  DEFAULTS:
    base: [zenpacklib.Component]

  RabbitMQAPI_Node:
    label: API Node

  RabbitMQAPI_VHost:
    label: DEFAULT RabbitMQ VHost
    relationships:
      rabbitMQAPI_Node:
        label: Node
        short_label: Node
      rabbitMQAPI_Exchanges:
        label: Exchanges
        order: 4
      rabbitMQAPI_Queues:
        label: Queues
        order: 5

  RabbitMQAPI_Exchange:
    label: API Exchange

  RabbitMQAPI_Queue:
    label: API Queue
"""

EXPECTED = ["{id: 'RabbitMQAPI_Node',\n                       dataIndex: 'rabbitMQAPI_Node',\n                       header: _t('Node'),\n                       width: 100,\n                       renderer: Zenoss.render.zenpacklib_ZenPacks_zenoss_RelationOverrides_entityLinkFromGrid,\n                       sortable: true}"]


class TestInheritedRelationOverrides(ZPLBaseTestCase):
    """Test fix for ZEN-21966
       ZenPackLib ignores label/short_label on relationship overrides for 1 to 1 contained relationships
    """
    yaml_doc = YAML_DOC

    def test_inherited_relation_overrides(self):
        cfg = self.configs.get('ZenPacks.zenoss.RelationOverrides').get('cfg')
        cls = cfg.classes.get('RabbitMQAPI_VHost')
        actual = cls.containing_js_columns
        self.assertEquals(EXPECTED, actual, 'containing_js_columns expected:\n{}\ngot:\n{}\n'.format(EXPECTED, actual))


def test_suite():
    """Return test suite for this module."""
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInheritedRelationOverrides))
    return suite

if __name__ == "__main__":
    from zope.testrunner.runner import Runner
    runner = Runner(found_suites=[test_suite()])
    runner.run()
