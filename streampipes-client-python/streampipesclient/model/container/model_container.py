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
import json

import pandas as pd

from abc import ABC, abstractmethod
from typing import List, Type

from pydantic import ValidationError

from streampipesclient.model.common import StreamPipesDataModelError
from streampipesclient.model.element import Element


class ModelContainer(ABC):

    def __init__(self, elements: List[Element]):
        self._elements = elements

    def __getitem__(self, position: int) -> Element:
        return self._elements[position]

    def __len__(self) -> int:
        return len(self._elements)

    @classmethod
    def from_json(cls, json_string: str) -> "ModelContainer":

        data = json.loads(json_string)

        if not type(data) == list:
            raise RuntimeError

        try:

            model_container = cls(
                elements=[cls._element_cls().parse_obj(list_item) for list_item in data]
            )
        except ValidationError as ve:
            raise StreamPipesDataModelError(validation_error=ve)

        return model_container

    @abstractmethod
    def to_pandas(self) -> pd.DataFrame:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _element_cls(cls) -> Type[Element]:
        raise NotImplementedError
