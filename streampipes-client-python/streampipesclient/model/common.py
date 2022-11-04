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

from typing import List, Optional

from pydantic import BaseModel, StrictStr, StrictInt, StrictBool, ValidationError


def snake_to_camel_case(snake_case_string: str) -> str:
    """
    Converts a string in snake_case format to camelCase style.
    """

    tokens = snake_case_string.split("_")

    return tokens[0] + "".join(t.title() for t in tokens[1:])


class BasicModel(BaseModel):
    element_id: Optional[StrictStr]

    class Config:
        alias_generator = snake_to_camel_case


class EventPropertyQualityDefinition(BasicModel):
    pass


class EventPropertyQualityRequirement(BasicModel):
    minimum_property_quality: Optional[EventPropertyQualityDefinition]
    maximum_property_quality: Optional[EventPropertyQualityDefinition]


class EventProperty(BasicModel):
    label: StrictStr
    description: StrictStr
    runtime_name: StrictStr
    required: StrictBool
    domain_properties: List[StrictStr]
    event_property_qualities: List[EventPropertyQualityDefinition]
    requires_event_property_qualities: List[EventPropertyQualityRequirement]
    property_scope: Optional[StrictStr]
    index: StrictInt
    runtime_id: Optional[StrictStr]
    runtime_type: Optional[StrictStr]
    measurement_unit: Optional[StrictStr]
    value_specification: Optional[StrictStr]


class EventSchema(BasicModel):
    event_properties: List[EventProperty]


class StreamPipesDataModelError(RuntimeError):

    def __init__(self, validation_error: ValidationError):
        super().__init__(
            self._generate_error_message(model=validation_error.model,
                                         error_description=validation_error.json(),
                                         )
        )

    @staticmethod
    def _generate_error_message(*, model: BasicModel, error_description: str) -> str:
        return f"\nOops, there seems to be a problem with our internal StreamPipes data model.\n" \
               f"This should not occur, but unfortunately did.\n" \
               f"Therefore, it would be great if you could report this problem as an issue at github.com/apache/incubator-streampipes.\n" \
               f"Please don't forget to include the following information:\n\n" \
               f"Affected Model class: {str(model)}\n" \
               f"Validation error log: {error_description}"
