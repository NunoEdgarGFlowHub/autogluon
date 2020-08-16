import logging

import pandas as pd
from pandas import DataFrame

from .abstract import AbstractFeatureGenerator
from ..feature_metadata import R_DATETIME, S_DATETIME_AS_OBJECT

logger = logging.getLogger(__name__)


class DatetimeFeatureGenerator(AbstractFeatureGenerator):
    def _fit_transform(self, X: DataFrame, **kwargs) -> (DataFrame, dict):
        X_out = self._transform(X)
        type_family_groups_special = dict(
            datetime_as_int=list(X_out.columns)
        )
        return X_out, type_family_groups_special

    def _transform(self, X: DataFrame) -> DataFrame:
        return self._generate_features_datetime(X)

    def _infer_features_in(self, X, y=None) -> list:
        datetime_features = self.feature_metadata_in.type_group_map_special[S_DATETIME_AS_OBJECT] + self.feature_metadata_in.type_group_map_raw[R_DATETIME]
        return datetime_features

    # TODO: Improve handling of missing datetimes
    def _generate_features_datetime(self, X: DataFrame) -> DataFrame:
        X_datetime = DataFrame(index=X.index)
        for datetime_feature in self.features_in:
            # TODO: Be aware: When converted to float32 by downstream models, the seconds value will be up to 3 seconds off the true time due to rounding error. If seconds matter, find a separate way to generate (Possibly subtract smallest datetime from all values).
            X_datetime[datetime_feature] = pd.to_datetime(X[datetime_feature])
            X_datetime[datetime_feature] = pd.to_numeric(X_datetime[datetime_feature])  # TODO: Use actual date info
            # X_datetime[datetime_feature] = pd.to_timedelta(X_datetime[datetime_feature]).dt.total_seconds()
            # TODO: Add fastai date features
        return X_datetime
