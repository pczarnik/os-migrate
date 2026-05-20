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
module: import_snapshot_create_dst_snapshot
short_description: Create a snapshot from a temporary volume on the destination cloud
extends_documentation_fragment:
  - os_migrate.os_migrate.openstack
version_added: "2.9.0"
author: "OpenStack tenant migration tools (@os-migrate)"
description:
  - "Create a volume snapshot on the destination cloud from a temporary volume"
  - "that received data via the detached volume migration pipeline."
  - "Applies the original snapshot name, description, and metadata."
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
      - ID of the destination temporary volume to create a snapshot from.
    required: true
    type: str
  snapshot_name:
    description:
      - Name for the destination snapshot (original snapshot name).
    required: true
    type: str
  snapshot_description:
    description:
      - Description for the destination snapshot.
    required: false
    type: str
    default: null
  snapshot_metadata:
    description:
      - Metadata dict for the destination snapshot.
    required: false
    type: dict
    default: {}
  timeout:
    description:
      - Timeout for snapshot creation, in seconds.
    required: false
    type: int
    default: 1800
"""

EXAMPLES = r"""
- name: Create destination snapshot from temp volume
  os_migrate.os_migrate.import_snapshot_create_dst_snapshot:
    cloud: dst
    volume_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    snapshot_name: "snapshot for vcbis25-1455-3o1c1s-swraid"
    snapshot_description: null
    snapshot_metadata: {}
  register: create_dst_snap
"""

RETURN = r"""
snapshot_id:
  description: ID of the created destination snapshot.
  returned: On success.
  type: str
  sample: "b2c3d4e5-f6a7-8901-bcde-f12345678901"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.os_migrate.os_migrate.plugins.module_utils import os_auth


def run_module():
    argument_spec = os_auth.openstack_full_argument_spec(
        volume_id=dict(type="str", required=True),
        snapshot_name=dict(type="str", required=True),
        snapshot_description=dict(type="str", default=None),
        snapshot_metadata=dict(type="dict", default={}),
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
    snapshot_name = module.params["snapshot_name"]
    snapshot_description = module.params["snapshot_description"]
    snapshot_metadata = module.params["snapshot_metadata"]
    timeout = module.params["timeout"]

    create_params = dict(
        volume_id=volume_id,
        name=snapshot_name,
        force=True,
    )
    if snapshot_description is not None:
        create_params["description"] = snapshot_description
    if snapshot_metadata:
        create_params["metadata"] = snapshot_metadata

    snap = conn.block_storage.create_snapshot(**create_params)
    conn.block_storage.wait_for_status(snap, status="available", wait=timeout)

    result["changed"] = True
    result["snapshot_id"] = snap["id"]

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
