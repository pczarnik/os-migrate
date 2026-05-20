The role import_snapshots
reads exported volume snapshots from the
snapshots YAML file, creates temporary volumes
from the snapshots on the source cloud, transfers
the data via the detached volume migration pipeline,
recreates snapshots on the destination cloud, and
cleans up temporary volumes on both sides.

For further information about the role import_snapshots refer to the
[official docs](https://os-migrate.github.io/os-migrate/roles/role-import_snapshots.html).
