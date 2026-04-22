#!/usr/bin/python

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.os_migrate.os_migrate.plugins.module_utils import filesystem
from ansible_collections.os_migrate.os_migrate.plugins.module_utils import snapshot
from ansible_collections.os_migrate.os_migrate.plugins.module_utils import os_auth

def run_module():
    argument_spec = os_auth.openstack_full_argument_spec(
        path=dict(type="str", required=True),
        snapshot_id=dict(type="str", required=True),
    )

    result = dict(
        changed=False,
        errors=[],
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        # TODO: Consider check mode. We'd fetch the resource and check
        # if the file representation matches it.
        # supports_check_mode=True,
    )

    conn = os_auth.get_connection(module)
    sdk_snapshot = conn.block_storage.get_snapshot(module.params["snapshot_id"])
    data = snapshot.Snapshot.from_sdk(conn, sdk_snapshot)

    result["changed"] = filesystem.write_or_replace_resource(
        module.params["path"], data
    )

    module.exit_json(**result)


def main():
    run_module()

if __name__ == "__main__":
    main()
