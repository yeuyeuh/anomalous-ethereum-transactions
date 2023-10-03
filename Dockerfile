# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /anomalous-ethereum-transactions

# Copy the Kedro project files into the container
COPY . /anomalous-ethereum-transactions

# Create and activate the Conda environment
RUN conda env create -f requirements/anomalous-transactions-env-freeze.yml
#SHELL ["conda", "activate", "anomalous-transactions-env-freeze"]
SHELL ["/bin/bash", "-c"]
RUN source activate anomalous-transactions-env-freeze

# Expose any necessary ports
EXPOSE 8080

# Specify the command to run when the container starts
CMD ["kedro", "run"]