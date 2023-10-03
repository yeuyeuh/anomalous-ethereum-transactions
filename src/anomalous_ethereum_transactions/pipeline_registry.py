"""Project pipelines."""
from typing import Dict

#inaki from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline



from .pipelines.data_processing import pipeline as dp
from .pipelines.data_science import pipeline as ds

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """

    data_processing_pipeline = dp.create_pipeline()
    data_science_pipeline = ds.create_pipeline()

    #inaki pipelines = find_pipelines()
    #inaki pipelines["__default__"] = sum(pipelines.values())
    #inaki return pipelines

    return  {
        "__default__": data_processing_pipeline +
        data_science_pipeline["pipeline_train"] +
        data_science_pipeline["pipeline_predict"],

        "data_recovery": data_processing_pipeline,

        "data_recovery_train_and_predict": data_processing_pipeline +
        data_science_pipeline["pipeline_train"] + 
        data_science_pipeline["pipeline_predict"],

        "data_recovery_predict": data_processing_pipeline +
        data_science_pipeline["pipeline_predict"],

        "only_train_and_predict": data_science_pipeline["pipeline_train"] + 
        data_science_pipeline["pipeline_predict"],
        
        "only_predict": data_science_pipeline["pipeline_predict"],
    }
