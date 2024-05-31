import sqlitecloud
from sqlitecloud.client import SqliteCloudClient,SqliteCloudAccount

try:
    account = SqliteCloudAccount('admin', 'KS6F2m5Fh1', 'ntr7kw2pik.sqlite.cloud', 'auto_harvestrasp', 8860)
    client = SqliteCloudClient(cloud_account=account)
    conn = client.open_connection()
except Exception as e:
    print(e)
    client=None
    conn=None
