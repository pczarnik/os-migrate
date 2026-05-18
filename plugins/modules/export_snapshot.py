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
module: export_snapshot
short_description: Export OpenStack volume snapshot
extends_documentation_fragment:
  - os_migrate.os_migrate.openstack
version_added: "2.9.0"
author: "OpenStack tenant migration tools (@os-migrate)"
description:
  - "Export OpenStack volume snapshot definition into an OS-Migrate YAML"
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
  path:
    description:
      - Resources YAML file to where snapshot will be serialized.
      - In case the resource file already exists, it must match the
        os-migrate version.
      - In case the resource of same type and name exists in the file,
        it will be replaced.
    required: true
    type: str
  name:
    description:
      - Name (or ID) of a Snapshot to export.
    required: true
    type: str
  cloud:
    description:
      - Cloud from clouds.yaml to use.
      - Required if 'auth' parameter is not used.
    required: false
    type: raw
"""

EXAMPLES = r"""
- name: Export mysnapshot into /opt/os-migrate/snapshots.yml
  os_migrate.os_migrate.export_snapshot:
    path: /opt/os-migrate/snapshots.yml
    name: mysnapshot
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
        name=dict(type="str", required=True),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    conn = os_auth.get_connection(module)
    sdk_snap = conn.block_storage.find_snapshot(
        module.params["name"], ignore_missing=False
    )
    snap = snapshot.Snapshot.from_sdk(conn, sdk_snap)

    result["changed"] = filesystem.write_or_replace_resource(
        module.params["path"], snap
    )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
