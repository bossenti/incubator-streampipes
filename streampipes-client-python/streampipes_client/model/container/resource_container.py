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

"""
General and abstract implementation for a resource container.
A resource container is a collection of resources returned by the StreamPipes API.
It is capable of parsing the response content directly into a list of queried resources.
Furthermore, the resource container makes them accessible in a pythonic manner.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Dict, List, Type

import pandas as pd
from pydantic import ValidationError
from streampipes_client.model.exception import (
    StreamPipesDataModelError,
    StreamPipesResourceContainerJSONError,
)

__all__ = [
    "ResourceContainer",
]

from streampipes_client.model.resource.resource import Resource


class ResourceContainer(ABC):
    """General and abstract implementation for a resource container.
    A resource container is a collection of resources returned by the StreamPipes API.
    It is capable of parsing the response content directly into a list of queried resources.
    Furthermore, the resource container makes them accessible in a pythonic manner.

    Parameters
    ----------
    resources: List[Resource]
        A list of resources (`model.resource.Resource`) to be contained in the `ResourceContainer`.

    """

    def __init__(self, resources: List[Resource]):
        self._resources = resources

    def __getitem__(self, position: int) -> Resource:
        return self._resources[position]

    def __len__(self) -> int:
        return len(self._resources)

    def __repr__(self):
        new_line = "\n"
        return f"{self.__class__.__name__}(resources=[{new_line.join([r.__repr__() for r in self._resources])}])"

    @classmethod
    @abstractmethod
    def _resource_cls(cls) -> Type[Resource]:
        """Returns the class of the resource that are bundled.

        Returns
        -------
        model.resource.Resource
        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def from_json(cls, json_string: str) -> ResourceContainer:
        """Creates a `ResourceContainer` from the given JSON string.

        Parameters
        ----------
        json_string: str
            The JSON string returned from the StreamPipes API.

        Returns
        -------
        ResourceContainer

        Raises
        ------
        StreamPipesDataModelError
            If a resource cannot be mapped to the corresponding Python data model.
        StreamPipesResourceContainerJSONError
            If JSON response cannot be parsed to a `ResourceContainer`.
        """

        # deserialize JSON string
        parsed_json = json.loads(json_string)

        # the ResourceContainer expects a list of items
        # raise an exception if the response does not be a list
        if not type(parsed_json) == list:
            raise StreamPipesResourceContainerJSONError(container_name=str(cls), json_string=json_string)
        try:

            resource_container = cls(resources=[cls._resource_cls().parse_obj(item) for item in parsed_json])
        except ValidationError as ve:
            raise StreamPipesDataModelError(validation_error=ve)

        return resource_container

    def to_dicts(self, use_source_names: bool = False) -> List[Dict]:
        """Returns the contained resources as list of dictionaries.

        Parameters
        ----------
        use_source_names: bool
            Determines whether the field names are named in Python style (=`False`) or
            as originally named by StreamPipes (=`True`).

        Returns
        -------
        List[Dict]]
        """
        return [resource.dict(by_alias=use_source_names) for resource in self._resources]

    def to_json(self) -> str:
        """Returns the resource container in the StreamPipes JSON representation.

        Returns
        -------
        JSON string
        """

        return json.dumps(self.to_dicts(use_source_names=True))

    @abstractmethod
    def to_pandas(self) -> pd.DataFrame:
        """Returns the resource container in representation of a Pandas Dataframe.

        Returns
        -------
        pd.DataFrame
        """
        raise NotImplementedError  # pragma: no cover
