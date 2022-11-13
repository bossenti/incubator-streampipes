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

from abc import abstractmethod

from pydantic import ValidationError

__all__ = [
    "StreamPipesDataModelError",
    "StreamPipesResourceContainerJSONError",
]


class StreamPipesBaseException(Exception):
    """Basic class for custom StreamPipes exceptions."""

    @abstractmethod
    def _generate_error_message(self, **kwargs):
        raise NotImplementedError  # pragma: no cover


class StreamPipesDataModelError(StreamPipesBaseException):
    """A custom exception to be raised when a validation error occurs
    during the parsing of StreamPipes API responses.

    Parameters
    ----------
    validation_error: ValidationError
        The validation error thrown by Pydantic during parsing.
    """

    def __init__(
        self,
        validation_error: ValidationError,
    ):
        self.validation_error = validation_error
        super().__init__(self._generate_error_message())

    def _generate_error_message(self) -> str:
        return (
            f"\nOops, there seems to be a problem with our internal StreamPipes data model.\n"
            f"This should not occur, but unfortunately did.\n"
            f"Therefore, it would be great if you could report this problem as an issue at "
            f"github.com/apache/incubator-streampipes.\n"
            f"Please don't forget to include the following information:\n\n"
            f"Affected Model class: {str(self.validation_error.model)}\n"
            f"Validation error log: {self.validation_error.json()}"
        )


class StreamPipesResourceContainerJSONError(StreamPipesBaseException):
    """A custom exception to be raised when the returned JSON string
    does not suit to the structure of resource container.

    Parameters
    ----------
    container: ResourceContainer
        The class of the resource container where the invalid data structure was detected.
    json_string: str
        The JSON string that has been tried to parse.
    """

    def __init__(
        self,
        container: "ResourceContainer",  # noqa: F821
        json_string: str,
    ):
        self.container = container
        self.json_string = json_string
        super().__init__(self._generate_error_message())

    def _generate_error_message(self) -> str:
        return (
            f"\nOops, there seems to be a problem when parsing the response of the StreamPipes API."
            f"This should not occur, but unfortunately did.\n"
            f"Therefore, it would be great if you could report this problem as an issue at "
            f"github.com/apache/incubator-streampipes.\n"
            f"Please don't forget to include the following information:\n\n"
            f"Affected container class: {str(self.container)}\n"
            f"JSON string: {self.json_string}"
        )
