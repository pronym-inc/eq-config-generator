import os
import shutil
from typing import List

from ini import Server, SERVERS


def sync_macros(servers: List[Server]):
    local_path = "C:\\Users\\Gregg\\AppData\\Local\\VeryVanilla\\Emu\\Release\\Macros"

    for file in os.listdir(local_path):
        if file.endswith(".mac") or file.endswith(".inc"):
            full_local = os.path.join(local_path, file)
            for server in servers:
                remote_path = os.path.join(server.mq_path, "Macros")
                full_other = os.path.join(remote_path, file)

                should_upload = False

                if os.path.exists(full_other):
                    local_mtime = os.path.getmtime(full_local)
                    remote_mtime = os.path.getmtime(full_other)

                    if remote_mtime <= local_mtime:
                        should_upload = True
                else:
                    should_upload = True

                if should_upload:
                    print(f"Uploading {full_other}")
                    shutil.copy(full_local, full_other)


if __name__ == '__main__':
    sync_macros(SERVERS[1:])
