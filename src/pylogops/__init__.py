import threading

# Local thread container instantiated here to be shared between all submodules in this package
# Note that thread.local() is not singleton!!!
# We use local thread container for sharing the transaction_id of request for logs
local_context = threading.local()
