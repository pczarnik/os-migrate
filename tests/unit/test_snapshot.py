from __future__ import absolute_import, division, print_function

__metaclass__ = type

import openstack
import unittest

from ansible_collections.os_migrate.os_migrate.plugins.module_utils import (
    const,
    snapshot,
)


def sdk_snapshot():
    return openstack.block_storage.v3.snapshot.Snapshot(
        created_at="2024-01-06T15:50:55Z",
        description="test snapshot",
        id="uuid-test-snap",
        metadata={"key1": "val1"},
        name="test-snap",
        project_id="uuid-test-project",
        size=10,
        status="available",
        updated_at="2024-01-06T15:51:00Z",
        user_id="uuid-test-user",
        volume_id="uuid-test-volume",
    )


def serialized_snapshot():
    return {
        const.RES_PARAMS: {
            "description": "test snapshot",
            "metadata": {"key1": "val1"},
            "name": "test-snap",
            "volume_type": "lvmdriver-1",
        },
        const.RES_INFO: {
            "created_at": "2024-01-06T15:50:55Z",
            "id": "uuid-test-snap",
            "project_id": "uuid-test-project",
            "size": 10,
            "status": "available",
            "updated_at": "2024-01-06T15:51:00Z",
            "user_id": "uuid-test-user",
            "volume_id": "uuid-test-volume",
            "volume_name": "test-volume",
        },
        const.RES_TYPE: "openstack.block_storage.Snapshot",
    }


def snapshot_refs():
    return {
        "volume_id": "uuid-test-volume",
        "volume_name": "test-volume",
        "volume_type": "lvmdriver-1",
    }


class Snapshot(snapshot.Snapshot):

    def _refs_from_ser(self, conn):
        return snapshot_refs()

    @staticmethod
    def _refs_from_sdk(conn, sdk_res):
        return snapshot_refs()


class TestSnapshot(unittest.TestCase):

    def test_serialize_snapshot(self):
        sdk_snap = sdk_snapshot()
        snap = Snapshot.from_sdk(None, sdk_snap)
        params, info = snap.params_and_info()

        self.assertEqual(snap.type(), "openstack.block_storage.Snapshot")
        self.assertEqual(params["description"], "test snapshot")
        self.assertEqual(params["metadata"], {"key1": "val1"})
        self.assertEqual(params["name"], "test-snap")
        self.assertEqual(params["volume_type"], "lvmdriver-1")

        self.assertEqual(info["created_at"], "2024-01-06T15:50:55Z")
        self.assertEqual(info["id"], "uuid-test-snap")
        self.assertEqual(info["project_id"], "uuid-test-project")
        self.assertEqual(info["size"], 10)
        self.assertEqual(info["status"], "available")
        self.assertEqual(info["updated_at"], "2024-01-06T15:51:00Z")
        self.assertEqual(info["user_id"], "uuid-test-user")
        self.assertEqual(info["volume_id"], "uuid-test-volume")
        self.assertEqual(info["volume_name"], "test-volume")

    def test_snapshot_sdk_params(self):
        snap = Snapshot.from_data(serialized_snapshot())
        refs = snap._refs_from_ser(None)
        sdk_params = snap._to_sdk_params(refs)

        self.assertEqual(sdk_params["description"], "test snapshot")
        self.assertEqual(sdk_params["metadata"], {"key1": "val1"})
        self.assertEqual(sdk_params["name"], "test-snap")
        self.assertNotIn("size", sdk_params)
        self.assertNotIn("status", sdk_params)
        self.assertNotIn("volume_id", sdk_params)
