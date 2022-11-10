<!--
  ~ Licensed to the Apache Software Foundation (ASF) under one or more
  ~ contributor license agreements.  See the NOTICE file distributed with
  ~ this work for additional information regarding copyright ownership.
  ~ The ASF licenses this file to You under the Apache License, Version 2.0
  ~ (the "License"); you may not use this file except in compliance with
  ~ the License.  You may obtain a copy of the License at
  ~
  ~    http://www.apache.org/licenses/LICENSE-2.0
  ~
  ~ Unless required by applicable law or agreed to in writing, software
  ~ distributed under the License is distributed on an "AS IS" BASIS,
  ~ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  ~ See the License for the specific language governing permissions and
  ~ limitations under the License.
  ~
-->

# StreamPipes client for Python

Apache StreamPipes meets Python! We are working highly motivated on a Python-based client to interact with StreamPipes.
Thus, we would like to unite the power of StreamPipes to easily connect to and read from several data sources, especially in the IoT domain,
and the amazing university of data analytics libraries in Python.

<br>

![StreamPipes Python logo](./docs/img/streampipes-python.png)

<br>

**:exclamation::exclamation::exclamation:IMPORTANT:exclamation::exclamation::exclamation:**
<br>
<br>
**The current version of this Python client is still in alpha phase at best**
<br>
**This means that it is still heavily under development, which may result in frequent and extensive API changes, unstable behavior, etc.**
<br>
**Please consider it only as paa sneak preview.**
<br>
<br>
**:exclamation::exclamation::exclamation:IMPORTANT:exclamation::exclamation::exclamation:**

### Get ready for development

1) Set up your Python environment
<br>
Create a virtual Python environment with a tool of your choice, here are some examples.
As a next step, install all required dependencies for the development, e.g. with pip:
```
pip install .[dev]  # or alternatively: pip install .[docs]
```
<br>
2) Install pre-commit hook
<br>
The pre-commit hook is run before every commit and takes care about code style,
linting, type hints, import sorting, etc.
Ensure to have the recent version of the pre-commit installed otherwise the CI build might fail:

```
pre-commit install
```
The definition of the pre-commit hook can found in [.pre-commit-config.yaml](.pre-commit-config.yaml).