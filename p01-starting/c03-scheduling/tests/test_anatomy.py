import hashlib
from os.path import dirname

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dag_cycle_tester import test_cycle as check_for_cycles

from c02_anatomy.echo_line_count import notify_cmd_str
from c02_anatomy.get_pictures import _get_pictures, read_img_from_file, download_one_picture
from dags import (
    d0203_Instantiate_DAG,
    d0204_Instantiate_bash_operator,
    d0206_invoking_python_operator,
    d02010_download_rocket_launches
)

path_to_data = f"{dirname(__file__)}/data"


def validate_dag(module):
    module_vars = vars(module)
    module_values = module_vars.values()
    for var in module_values:
        if isinstance(var, DAG):
            assert var
            print(var)
            check_for_cycles(var)


def test_d0203_instantiate_dag():
    validate_dag(d0203_Instantiate_DAG)


def test_d0204_instantiate_bash_operator():
    validate_dag(d0204_Instantiate_bash_operator)


def test_d0206_invoking_python_operato():
    validate_dag(d0206_invoking_python_operator)


def test_d02010_download_rocket_launches():
    validate_dag(d02010_download_rocket_launches)


def test_read_img_from_file():
    result = read_img_from_file(f"{path_to_data}/input/cz-8_liftoff_2_image_20240315183218.jpg")
    checksum = hashlib.md5(result).hexdigest()
    assert checksum == "fe294c6a0f9bd2efa9142dd204017871"


def test_download_launches():
    curl_command_list = [
        "curl",
        "-o", f"{path_to_data}/output/launches.json",
        "-L", "https://ll.thespacedevs.com/2.0.0/launch/upcoming"
    ]
    curl_command_str = " ".join(curl_command_list)
    strat = BashOperator(task_id="download_launches", bash_command=curl_command_str)
    strat.execute({})


def test_download_one_picture():
    download_one_picture("https://spacelaunchnow-prod-east.nyc3.digitaloceanspaces.com/media/images/cz-8_liftoff_2_image_20240315183218.jpg")


def test_notify():
    strat = BashOperator(task_id="notify", bash_command=notify_cmd_str)
    strat.execute({})
