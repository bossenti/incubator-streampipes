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
import logging
import sys
from dataclasses import dataclass
from typing import Dict, Optional, Union, Type

import requests

from streampipesclient.client.credentials import CredentialProvider
from streampipesclient.endpoints.data_lake_measure import DataLakeMeasureEndpoint

logger = logging.getLogger(__name__)


@dataclass
class StreamPipesClientConfig:
    """

    """

    credential_provider: CredentialProvider
    host_address: str
    https_disabled: Optional[bool] = False
    port: Optional[int] = 80


class StreamPipesClient:

    def __init__(self,
                 *,
                 client_config: StreamPipesClientConfig,
                 logging_level: int = logging.INFO,
                 ):
        self.client_config = client_config

        self.request_session = requests.Session()
        self.request_session.headers.update(self.http_headers)

        self._set_up_logging(logging_level=logging_level)

        # endpoints
        self.dataLakeMeasureApi = DataLakeMeasureEndpoint(parent_client=self)

    @staticmethod
    def _set_up_logging(*, logging_level: int) -> None:
        logging.basicConfig(
            level=logging_level,
            stream=sys.stdout,
            format="%(asctime)s - %(name)s - [%(levelname)s] - [%(filename)s:%(lineno)d] [%(funcName)s] - %(message)s",
        )

        logger.info(f"Logging successfully initialized with logging level {logging.getLevelName(logging_level)}.")

    @classmethod
    def create(cls, *, client_config: StreamPipesClientConfig, logging_level: int = logging.INFO):
        return cls(client_config=client_config, logging_level=logging_level)

    @property
    def http_headers(self) -> Dict[str, str]:
        return self.client_config.credential_provider.make_headers(
            {
                "Application": "application/json"
            }
        )

    @property
    def base_api_path(self) -> str:
        return f"{'http://' if self.client_config.https_disabled else 'https://'}" \
               f"{self.client_config.host_address}:" \
               f"{self.client_config.port}/streampipes-backend/"
