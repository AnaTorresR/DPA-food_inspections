import luigi
import luigi.contrib.s3
from luigi.contrib.postgres import CopyToTable
from src.pipeline.ingesta_test_task import TestIngestaTask
from src.utils.general import get_s3_credentials, get_db_credentials
from src.utils import constants
import pickle

# PYTHONPATH='.' luigi --module src.pipeline.ingesta_metadata_task IngestaMetadataTask --ingesta consecutiva --year 2021 --month 04 --day 15 --local-scheduler

class IngestaMetadataTask(CopyToTable):
    ingesta = luigi.Parameter()
    year = luigi.Parameter()
    month = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return {
        'TestIngestaTask': TestIngestaTask(self.ingesta, self.year, self.month, self.day)}

    credentials = get_db_credentials('conf/local/credentials.yaml')

    user=credentials['user']
    password=credentials['pass']
    host=credentials['host']
    port=credentials['port']
    database=credentials['db']

    table = 'metadata'

    columns = [("Task", "VARCHAR"),
               ("INGESTION", "VARCHAR"),
               ("FECHA", "TIMESTAMP WITHOUT TIME ZONE"),
               ("AUTOR", "VARCHAR")]

    def rows(self):
        date = str(self.year + '-' + self.month + '-' + self.day)
        r = [("Ingesta","Ingesta {}".format(self.ingesta), date , 'Equipo 6')]
        for element in r:
            yield element
