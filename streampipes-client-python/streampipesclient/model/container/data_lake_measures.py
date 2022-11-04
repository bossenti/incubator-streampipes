import pandas as pd

from streampipesclient.model.container import ModelContainer
from streampipesclient.model.element.data_lake_measure import DataLakeMeasure


class DataLakeMeasures(ModelContainer):

    @classmethod
    def _element_cls(cls):
        return DataLakeMeasure

    def to_pandas(self) -> pd.DataFrame:
        pass