#!/usr/bin/python


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: import_snapshot_cleanup
short_description: Delete a temporary volume used during snapshot migration
extends_documentation_fragment:
  - os_migrate.os_migrate.openstack
version_added: "2.9.0"
author: "OpenStack tenant migration tools (@os-migrate)"
description:
  - "Delete a temporary volume that was created during snapshot migration."
  - "Called once with source cloud credentials to delete the source temp volume,"
  - "and once with destination credentials to delete the destination temp volume."
options:
  auth:
    description:
      - Dictionary with parameters for chosen auth type.
      - Required if 'cloud' parameter is not used.
    required: false
    type: dict
  auth_type:
    description:
      - Auth type plugin for OpenStack. Can be omitted if using password authentication.
    required: false
    type: str
  region_name:
    description:
      - OpenStack region name. Can be omitted if using default region.
    required: false
    type: str
  cloud:
    description:
      - Cloud from clouds.yaml to use.
      - Required if 'auth' parameter is not used.
    required: false
    type: raw
  volume_id:
    description:
      - ID of the temporary volume to delete.
    required: true
    type: str
  timeout:
    description:
      - Timeout for volume deletion, in seconds.
    required: false
    type: int
    default: 1800
"""

EXAMPLES = r"""
- name: Delete source temp volume
  os_migrate.os_migrate.import_snapshot_cleanup:
    cloud: src
    volume_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

- name: Delete destination temp volume
  os_migrate.os_migrate.import_snapshot_cleanup:
    cloud: dst
    volume_id: "b2c3d4e5-f6a7-8901-bcde-f12345678901"
"""

RETURN = r"""
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.os_migrate.os_migrate.plugins.module_utils import os_auth


def run_module():
    argument_spec = os_auth.openstack_full_argument_spec(
        volume_id=dict(type="str", required=True),
        timeout=dict(type="int", default=1800),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    conn = os_auth.get_connection(module)

    volume_id = module.params["volume_id"]
    timeout = module.params["timeout"]

    volume = conn.block_storage.find_volume(volume_id, ignore_missing=True)
    if volume is not None:
        conn.block_storage.delete_volume(volume, wait=True, timeout=timeout)
        result["changed"] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
