import re
from google.cloud import storage

# Kubernetes release binaries are published in a google cloud bucket
# The logic was found on https://github.com/chuckha/downloadkubernetes

# https://stackoverflow.com/a/2574090/401041
storage_client = storage.Client.create_anonymous_client()
bucket = storage_client.get_bucket("kubernetes-release")
kubernetes_release_blobs = storage_client.list_blobs(bucket, prefix="release/stable-")

# https://cloud.google.com/storage/docs/listing-objects#storage-list-objects-python
version_regex = re.compile("release/stable-(\d+\.\d+).txt")
version_list = []
for blob in kubernetes_release_blobs:
    version_info = version_regex.findall(blob.name)
    if version_info:
        version_list.append(version_info[0])

# https://stackoverflow.com/a/2574090/401041
version_list.sort(key=lambda s: list(map(int, s.split("."))))
latest_major_version = version_list[-1]
latest_full_version_blob = bucket.blob(f"release/stable-{latest_major_version}.txt")
latest_full_version = latest_full_version_blob.download_as_string().decode()
print("Latest kubernetes version is", latest_full_version)
