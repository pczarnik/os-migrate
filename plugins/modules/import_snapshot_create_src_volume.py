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
module: import_snapshot_create_src_volume
short_description: Create a temporary volume from a snapshot on the source cloud
extends_documentation_fragment:
  - os_migrate.os_migrate.openstack
version_added: "2.9.0"
author: "OpenStack tenant migration tools (@os-migrate)"
description:
  - "Create a temporary volume from a volume snapshot on the source cloud."
  - "This volume is used as the source for the detached volume migration pipeline."
  - "The volume should be cleaned up after the snapshot is recreated on the destination."
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
  snapshot_id:
    description:
      - ID of the snapshot to create a volume from.
    required: true
    type: str
  volume_name_prefix:
    description:
      - Prefix for the temporary volume name.
      - The full name will be prefix + snapshot_id.
    required: false
    type: str
    default: "os-migrate-snap-"
  volume_type:
    description:
      - Volume type for the temporary volume.
    required: false
    type: str
    default: null
  timeout:
    description:
      - Timeout for volume creation, in seconds.
    required: false
    type: int
    default: 1800
"""

EXAMPLES = r"""
- name: Create temp volume from snapshot
  os_migrate.os_migrate.import_snapshot_create_src_volume:
    cloud: src
    snapshot_id: "73809910-8800-4d79-8b69-078ffa613de8"
    volume_name_prefix: "os-migrate-snap-"
    volume_type: "tripleo-ceph"
  register: create_src_vol
"""

RETURN = r"""
volume_id:
  description: ID of the created temporary volume.
  returned: On success.
  type: str
  sample: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.os_migrate.os_migrate.plugins.module_utils import os_auth


def run_module():
    argument_spec = os_auth.openstack_full_argument_spec(
        snapshot_id=dict(type="str", required=True),
        volume_name_prefix=dict(type="str", default="os-migrate-snap-"),
        volume_type=dict(type="str", default=None),
        timeout=dict(type="int", default=1800),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    conn = os_auth.get_connection(module)

    snapshot_id = module.params["snapshot_id"]
    prefix = module.params["volume_name_prefix"]
    volume_type = module.params["volume_type"]
    timeout = module.params["timeout"]

    volume_name = f"{prefix}{snapshot_id}"

    snapshot = conn.block_storage.get_snapshot(snapshot_id)

    create_params = dict(
        snapshot_id=snapshot_id,
        name=volume_name,
        size=snapshot["size"],
    )
    if volume_type:
        create_params["volume_type"] = volume_type

    volume = conn.block_storage.create_volume(**create_params)
    conn.block_storage.wait_for_status(volume, status="available", wait=timeout)

    result["changed"] = True
    result["volume_id"] = volume["id"]

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
