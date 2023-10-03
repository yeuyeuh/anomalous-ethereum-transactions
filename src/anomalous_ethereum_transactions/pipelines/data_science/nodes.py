"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.13
"""

import logging
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import plotly.express as px



def train_anomalousDetection(tx_df, features):
  """Train an Isolation Forest model to detect anomalous transactions

  Args:
      tx_df: transaction df
      features: features used by the model

  Returns:
      trained model
  """
  
  X_train = tx_df[features].to_numpy()

  clf = IsolationForest(random_state=0)
  clf.fit(X_train)
  return clf


def predict_anomalousDetection(tx_df, clf, features):
  """Use the previously trained model to predict the anomalous transactions

  Args:
      tx_df: transaction df
      clf: model already trained
      features: features used by the model

  Returns:
      transaction df with prediction values
  """

  logger = logging.getLogger(__name__)

  X_train = tx_df[features].to_numpy()

  y=clf.predict(X_train)
  tx_df["Anomalous"] = y
  tx_df.Anomalous = tx_df.Anomalous.apply(lambda x: False if x==1 else True )

  logger.info("List of anomalous transactions: %s", tx_df.index[tx_df.Anomalous])
  
  return tx_df

def DimensionalityReductionPlot(tx_df, features):
  """Run a tSNE on the tx data and color the plot by anomalous prediction

  Args:
      tx_df: transaction df with prediction values
      features: features used for tSNE

  Returns:
      tSNE plot (inside data/08_reporting)
  """

  logger = logging.getLogger(__name__)
  logger.info(f"Plot tSNE colored by anomalous transactions")

  X_train = tx_df[features].to_numpy()
  scaler = StandardScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_embedded = TSNE(n_components=2, perplexity=15).fit_transform(X_train_scaled)
  

  tx_df["tSNE_x"]=X_embedded[:,0]
  tx_df["tSNE_y"]=X_embedded[:,1]

  fig = px.scatter(tx_df, x="tSNE_x", y="tSNE_y", color="Anomalous", 
                  hover_data=features+["hash"],
                  title='tSNE on the predicted data (colored by anomalous transaction prediction).<br>Only the features used by the anomalous detection model are used.<br>The features have been standard scaled')
  fig.update_yaxes(
      scaleanchor = "x",
      scaleratio = 1,
    )

  path_reporting = 'data/08_reporting'
  fig.write_html(f"{path_reporting}/tSNE_on_predicted_data.html")
  fig.write_image(f"{path_reporting}/tSNE_on_predicted_data.png")

  return None
