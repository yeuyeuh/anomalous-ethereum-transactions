"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.13
"""
from kedro.pipeline import Pipeline, pipeline, node
from kedro.config import ConfigLoader

from .nodes import get_blocks_data

def create_pipeline(**kwargs) -> Pipeline:
    conf_loader = ConfigLoader(conf_source="conf")
    parameters = conf_loader.get("parameters*")

    return pipeline(
        [
            node(
                func=get_blocks_data,
                inputs=["params:block_number_start", "params:block_number_end","params:infura_API_key"],
                outputs="tx_df",
            ),
        ]
    )
