from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    import openstack

    HAS_OPENSTACK = True
    OPENSTACK_SDK_SNAPSHOT = openstack.block_storage.v3.snapshot.Snapshot
except ImportError:
    HAS_OPENSTACK = False
    OPENSTACK_SDK_SNAPSHOT = None

from ansible_collections.os_migrate.os_migrate.plugins.module_utils import (
    const,
    reference,
    osm_resource,
)


class Snapshot(osm_resource.Resource):

    resource_type = const.RES_TYPE_SNAPSHOT
    sdk_class = OPENSTACK_SDK_SNAPSHOT

    info_from_sdk = [
        "created_at",
        "id",
        "project_id",
        "size",
        "status",
        "updated_at",
        "user_id",
        "volume_id",
    ]
    info_from_refs = [
        "volume_name",
    ]
    params_from_sdk = [
        "description",
        "metadata",
        "name",
    ]
    params_from_refs = [
        "volume_type",
    ]
    sdk_params_from_refs = []

    @staticmethod
    def _create_sdk_res(conn, sdk_params):
        return conn.block_storage.create_snapshot(**sdk_params)

    @staticmethod
    def _find_sdk_res(conn, name_or_id, filters=None):
        return conn.block_storage.find_snapshot(name_or_id, **(filters or {}))

    @staticmethod
    def _refs_from_sdk(conn, sdk_res):
        refs = {}
        refs["volume_id"] = sdk_res["volume_id"]
        volume = conn.block_storage.get_volume(sdk_res["volume_id"])
        refs["volume_name"] = volume["name"]
        refs["volume_type"] = volume["volume_type"]
        return refs

    def _refs_from_ser(self, conn):
        refs = {}
        refs["volume_id"] = self.info()["volume_id"]
        refs["volume_name"] = self.info()["volume_name"]
        refs["volume_type"] = self.params()["volume_type"]
        return refs

    @staticmethod
    def _update_sdk_res(conn, sdk_res, sdk_params):
        return conn.block_storage.update_snapshot(sdk_res, **sdk_params)
