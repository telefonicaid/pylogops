# pylogops
Really simple json formatter for python projects.

## Installation

```bash
pip install pylogps
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

Pylogps includes a filter and a local_context to support using a context holding information about a correlator (corr), transaction (trans) and operation (op).
If you include the values using local_context, those fields will be available in formatter.

```py
```

local_context is a thread.local() that is shared in current thread for all modules; typically you will include the values in a middleware or some kind of transversal module.


### Customizing json fields

## License

Copyright 2014, 2015 [Telefonica Investigación y Desarrollo, S.A.U](http://www.tid.es)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
