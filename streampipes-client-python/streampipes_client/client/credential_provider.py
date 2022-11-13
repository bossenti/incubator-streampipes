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
Implementation of credential providers.
A credential provider supplies the specified sort of credentials in the appropriate HTTP header format.
The headers are then used by the client to connect to StreamPipes.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional

__all__ = [
    "CredentialProvider",
    "StreamPipesApiKeyCredentials",
]


class CredentialProvider(ABC):
    """Abstract implementation of a credential provider.
    Must be inherited by all credential providers.
    """

    def make_headers(self, http_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Creates the HTTP headers for the specific credential provider.
        Concrete authentication headers must be defined in the implementation of a credential provider.

        Parameters
        ----------
        http_headers: Optional[Dict[str, str]]
            Additional HTTP headers the generated headers are extended by.

        Returns
        -------
        Dictionary with header information as string key-value pairs.

        """
        if http_headers is None:
            http_headers = {}

        http_headers.update(self._authentication_headers)

        return http_headers

    @property
    @abstractmethod
    def _authentication_headers(self) -> Dict[str, str]:
        """Provides the HTTP headers used for the authentication with the concrete `CredentialProvider`.

        Returns
        -------
        Dictionary with authentication headers as string key-value pairs.

        """
        raise NotImplementedError  # pragma: no cover


class StreamPipesApiKeyCredentials(CredentialProvider):
    """A Credential provider that allows authentication via a StreamPipes API Token.
    This token can be generated via the StreamPipes UI (see how in the project's README).

    Parameters
    ----------
    username: str
        The username to which the API token is granted, e.g., `demo-user@streampipes.apche.org`.
    api_key: str
        The StreamPipes API key as it is displayed in the UI.

    Examples
    --------
    see `StreamPipesClient`

    References
    ----------
    [^1]: [StreamPipes Python Client README]
    (https://github.com/apache/incubator-streampipes/blob/dev/streampipes-client-python/README.md#%EF%B8%8F-quickstart)
    """

    def __init__(
        self,
        username: str,
        api_key: str,
    ):
        self.username = username
        self.api_key = api_key

    @property
    def _authentication_headers(self) -> Dict[str, str]:
        """Provides the HTTP headers used for the authentication with the API token.

        Returns
        -------
        Dictionary with authentication headers as string key-value pairs.

        """
        return {
            "X-API-User": self.username,
            "X-API-Key": self.api_key,
        }
