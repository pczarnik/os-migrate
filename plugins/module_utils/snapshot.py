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
    exc,
    const,
    osm_resource,
)


class Snapshot(osm_resource.Resource):

    resource_type = const.RES_TYPE_SNAPSHOT
    sdk_class = OPENSTACK_SDK_SNAPSHOT

    info_from_sdk = [
        "created_at",
        "id",
        "size",
        "status",
        "updated_at",
        "volume_id",
    ]
    params_from_sdk = [
        "name",
        "description",
    ]

    def create_or_update(self, conn, filters=None):
        raise exc.Unsupported(
            "Direct Snapshot.create_or_update call is unsupported."
        )

    def sdk_params(self, conn):
        """Return creation SDK params which are editable by the user in the
        serialized workloads file. Other SDK params will be provided
        directly by the migration procedure and cannot be changed by
        the user.
        """
        # Presently we have nothing in refs, this is just to follow
        # the conventional approach.
        refs = self._refs_from_ser(conn)
        return self._to_sdk_params(refs)
