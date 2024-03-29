import pandas as pd
import luigi
from datetime import date
from datetime import timedelta
from src.pipeline.cleaning_metadata_task import CleaningMetadataTask
from luigi.contrib.postgres import CopyToTable
from src.utils.general import get_db_credentials, get_db_conn, select_clean_features
from src.utils.utils_notebook.feature_engineering import feature_engineering

# PYTHONPATH='.' luigi --module src.pipeline.feature_engineering_task FETask --ingesta consecutiva --year 2021 --month 03 --day 15 --local-scheduler

class FETask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return {'CleaningMetadataTask': CleaningMetadataTask(self.ingesta, self.year, self.month, self.day)}

    credentials = get_db_credentials('conf/local/credentials.yaml')

    user=credentials['user']
    password=credentials['pass']
    host=credentials['host']
    port=credentials['port']
    database=credentials['db']

    table = 'semantic.features'

    columns = [("facility_type", "varchar"),
    ("risk", "varchar"),
    ("zip", "integer"),
    ("inspection_date", "timestamp without time zone"),
    ("inspection_type", "varchar"),
    ("violations", "varchar"),
    ("last_inspection", "smallint"),
    ("first_inspection", "smallint"),
    ("label", "smallint")]

    def rows(self):

       	credentials = 'conf/local/credentials.yaml'

        today = date.today()
        delta_date = today - timedelta(days=7)

        df = select_clean_features(credentials, delta_date)

        df = feature_engineering(df)

        r = df.to_records(index = False)

        for element in r:
            yield element

