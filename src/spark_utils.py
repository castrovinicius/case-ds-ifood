"""Utilitários para criação da sessão Spark em ambiente local (Windows).

No Databricks a sessão spark já vem criada; aqui replicamos o mínimo
necessário para rodar o mesmo código localmente.
"""

import os
from pathlib import Path

from pyspark.sql import SparkSession

# Raiz do projeto (pasta que contém src/, notebooks/, data/)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

_DEFAULT_JAVA_HOME = r"C:\Users\vinic\.jdks\jdk-17.0.19+10" # modifique para o seu JDK 17 local
_DEFAULT_HADOOP_HOME = r"C:\Users\vinic\.hadoop" # modifique para o seu winutils/hadoop local


def get_spark(app_name: str = "ifood-case") -> SparkSession:
    """Cria (ou retorna) uma SparkSession local.

    Configura JAVA_HOME/HADOOP_HOME caso não estejam definidos no ambiente,
    o que é necessário para o Spark funcionar no Windows (winutils).
    """
    os.environ.setdefault("JAVA_HOME", _DEFAULT_JAVA_HOME)
    os.environ.setdefault("HADOOP_HOME", _DEFAULT_HADOOP_HOME)
    hadoop_bin = os.path.join(os.environ["HADOOP_HOME"], "bin")
    if hadoop_bin not in os.environ["PATH"]:
        os.environ["PATH"] = hadoop_bin + os.pathsep + os.environ["PATH"]

    spark = (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.shuffle.partitions", "8")  # dataset pequeno; evita overhead do default (200)
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark


def collect_pd(sdf):
    """Coleta um DataFrame Spark (pequeno!) como pandas.

    Usa collect() + asDict() em vez de toPandas() para não depender da
    compatibilidade da conversão interna do PySpark com pandas 3.x.
    Usar apenas para agregados/amostras destinados a exibição e gráficos.
    """
    import pandas as pd

    return pd.DataFrame([row.asDict(recursive=True) for row in sdf.collect()])
