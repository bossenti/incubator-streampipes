#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import Optional

from pydantic import StrictStr, StrictBool

from streampipesclient.model.common import EventSchema
from streampipesclient.model.element import Element


class DataLakeMeasure(Element):
    measure_name: StrictStr
    timestamp_field: StrictStr
    event_schema: EventSchema
    pipeline_id: Optional[StrictStr]
    pipeline_name: Optional[StrictStr]
    pipeline_is_running: StrictBool
    schema_version: StrictStr
