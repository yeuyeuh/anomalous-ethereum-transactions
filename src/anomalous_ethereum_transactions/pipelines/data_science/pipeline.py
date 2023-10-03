"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, pipeline, node

from .nodes import (
    train_anomalousDetection,
    predict_anomalousDetection, 
    DimensionalityReductionPlot
)

def create_pipeline(**kwargs) -> Pipeline:
    
    pipeline_train = Pipeline(
        [
            node(
                func=train_anomalousDetection,
                inputs=["tx_df","params:features_anomalous_detection_model"],
                outputs="anomalous_detection_model",
            ),
        ]
    )

    pipeline_predict = Pipeline(
        [
            node(
                func=predict_anomalousDetection,
                inputs=["tx_df","anomalous_detection_model","params:features_anomalous_detection_model"],
                outputs="tx_wPredictions_df",
            ),
            node(
                func=DimensionalityReductionPlot,
                inputs=["tx_wPredictions_df","params:features_anomalous_detection_model"],
                outputs=None,
            ),
        ]
    )

    return {
        "pipeline_train": pipeline_train,
        "pipeline_predict":pipeline_predict,
    }