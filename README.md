# pylogops
Really simple json formatter for python projects.

### Status
[![Build Status](https://travis-ci.org/telefonicaid/pylogops.svg?branch=master)](https://travis-ci.org/telefonicaid/pylogops)

## Installation

```bash
pip install pylogps
```

if you want use with python2.6 you must install the backport ordereddict as well:

```bash
pip install ordereddict
```


## Basic usage
You will have to specify the formatter *JsonFormatter* in any handler that you use in standar python logging:

```py
import logging
import time
from pylogops.logger import JsonFormatter

file_handler = logging.FileHandler('/tmp/my_log.log', encoding='UTF-8')
file_handler.setFormatter(JsonFormatter(converter=time.localtime))
logging.basicConfig()
logger = logging.getLogger("my_logger")
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
logger.info("Msg")

```
this will produce a log in json:
```json
{"time": "2015-12-09T17:46:01.160Z", "lvl": "INFO", "corr": null, "trans": null, "op": null, "comp": "<stdin>", "msg": "Msg"}
```

To log in console change FileHandler by an StreamHandler:

```py
import logging
import time
from pylogops.logger import JsonFormatter

console_handler = logging.StreamHandler()
console_handler.setFormatter(JsonFormatter(converter=time.localtime))
logging.basicConfig()
logger = logging.getLogger("my_logger")
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)
logger.info("Msg")
```

**pylogps** by default generate all the upper fields in json output, but you can select to remove null fields:

```py
import logging
import time
from pylogops.logger import JsonFormatter

file_handler = logging.FileHandler('/tmp/my_log.log', encoding='UTF-8')
file_handler.setFormatter(JsonFormatter(remove_blanks=True))
logging.basicConfig()
logger = logging.getLogger("my_logger")
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
logger.info("Msg")


```
this will produce a log in json:
```json
{"time": "2015-12-09T16:57:00.784Z", "lvl": "INFO", "comp": "<stdin>", "msg": "Msg"}
```

You can configure the formatter in any way provided by python logging library, e.g (dictConfig, fileConfig, …). You can check unit tests directory for some example.

## Advanced usage

### Context support

#### Tracking filter

Pylogps includes a filter and a local_context to support using a context holding information about a correlator (corr), transaction (trans) and operation (op).
If you include the values using local_context, those fields will be available in formatter. You need to add a Filter:

```py
import logging
import time
from pylogops.logger import TrackingFilter, JsonFormatter

file_handler = logging.FileHandler('/tmp/my_log.log', encoding='UTF-8')
file_handler.addFilter(TrackingFilter())
file_handler.setFormatter(JsonFormatter(remove_blanks=True))
logging.basicConfig()
logger = logging.getLogger("my_logger")
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


from pylogops import local_context
local_context.trans = "trans"
local_context.corr = "corr"
local_context.op = "op"

logger.info("Msg")
```
This will produce the json log:
```json
{"time": "2015-12-10T15:23:52.117Z", "lvl": "INFO", "corr": "corr", "trans": "trans", "op": "op", "comp": "<stdin>", "msg": "Msg"}
```

local_context is a thread.local() that is shared in current thread for all modules; typically you will include the values in a middleware or some kind of transversal module.

### Customizing json fields

You can specify the fields for output in json in this way:
```py
import logging
import time
from pylogops.logger import JsonFormatter

file_handler = logging.FileHandler('/tmp/my_log.log', encoding='UTF-8')
file_handler.setFormatter(JsonFormatter(keys_fmt=[('lvl', 'levelname'), ('msg', 'message')]))
logging.basicConfig()
logger = logging.getLogger("my_logger")
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
logger.info("Msg")


```
this will produce a log in json:

```json
{"lvl": "INFO", "msg": "Msg"}
```

Note that if you set this formatter field you should provide ALL required fields for json (even those without change).

#### Static filter

A filter provided to include static content to python logger. All keyword args used in the initialization of the filter
 will be automatically provided as values for any formatter.

```py
import logging
import time
from pylogops.logger import StaticFilter, JsonFormatter

console_handler = logging.StreamHandler()
console_handler.addFilter(StaticFilter(version="1.2"))
console_handler.setFormatter(JsonFormatter(remove_blanks=True, keys_fmt=[('lvl', 'levelname'), ('msg', 'message'), ('version', 'version')]))
logger = logging.getLogger("my_logger")
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

logger.info("Msg")
```
This will produce the json log:
```json
{"time": "2015-12-10T15:23:52.117Z", "lvl": "INFO", "version": "1.2", "comp": "<stdin>", "msg": "Msg"}
```

 
### Upload to pypi

Use twine to upload the package and publish in pypi.

```
pip install twine
```

Prepare the package:

```
python3 setup.py sdist bdist_wheel
```

Upload:

```
twine upload dist/*
```

## License

Copyright 2014, 2015 [Telefonica Investigación y Desarrollo, S.A.U](http://www.tid.es)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
