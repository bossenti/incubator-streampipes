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
from http import HTTPStatus
import logging
from abc import ABC, abstractmethod
from typing import Tuple, Type, Callable

import requests
from requests import Response
from requests.exceptions import HTTPError

from streampipesclient.model.container import ModelContainer
from streampipesclient.model.element import Element

logger = logging.getLogger(__name__)

status_code_to_log_message = {
    401: "\nThe StreamPipes Backend returned an unauthorized error.\n"
         "Please check your user name and/or password to be correct.",
    403: "\nThere seems to be an issue with the accees rights of the given user and the ressource you queried.\n"
         "Apparently, this user is not allowd to query the resource.\n"
         "Please check the user's permissions or contact your StreamPipes admin.",
    **dict.fromkeys(
        [404, 405],
        "\nOops, there seems to be an issue with the Python Client calling the API inappropriately.\n"
        "This should not happen, but unfortunately did.\n"
        "If you don't mind, it would be awesome to let us know by creating an issue at github.com/apache/incubator-streampipes.\n"
        "Please paste the following information to the issue description:\n\n")
}


class APIEndpoint(ABC):

    def __init__(self, parent_client: "StreamPipesClient"):
        self._parent_client = parent_client

    @property
    @abstractmethod
    def _relative_api_path(self) -> Tuple[str]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _container_cls(cls) -> Type[ModelContainer]:
        raise NotImplementedError

    def _make_request(self,
                      *,
                      request_method: Callable[..., Response],
                      url: str,
                      ) -> Response:

        response = request_method(url=url)

        try:
            response.raise_for_status()
        except HTTPError as err:

            status_code = err.response.status_code

            log_message = status_code_to_log_message[err.response.status_code]

            if status_code in [HTTPStatus.METHOD_NOT_ALLOWED.numerator, HTTPStatus.NOT_FOUND.numerator]:
                log_message += f"url: {err.response.url}\nstatus code: {err.response.status_code}"

            logger.debug(err.response.text)
            raise HTTPError(log_message) from err

        else:
            logger.debug("Successfully retrieved resources from %s.", url)
            logger.info("Successfully retrieved all resources.")

        return response

    def create_api_path(self) -> str:
        return f"{self._parent_client.base_api_path}{'/'.join(api_path for api_path in self._relative_api_path)}"

    def all(self) -> ModelContainer:

        response = self._make_request(
            request_method=self._parent_client.request_session.get,
            url=self.create_api_path()
        )
        return self._container_cls().from_json(json_string=response.text)

    def get(self, *, identifier: str) -> Element:

        # equals to download
        # needs further considerations
        pass
