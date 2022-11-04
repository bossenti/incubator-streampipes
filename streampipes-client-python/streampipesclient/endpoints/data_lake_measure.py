from typing import List

from streampipesclient.endpoints.endpoint import APIEndpoint
from streampipesclient.model.container import ModelContainer
from streampipesclient.model.container.data_lake_measures import DataLakeMeasures
from streampipesclient.model.element import Element
from streampipesclient.model.element.data_lake_measure import DataLakeMeasure


class DataLakeMeasureEndpoint(APIEndpoint):

    @classmethod
    def _container_cls(cls):
        return DataLakeMeasures

    @property
    def _relative_api_path(self):
        return "api", "v4", "datalake", "measurements"
