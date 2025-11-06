# Project Guide

## High level architecture

- We will be ingesting data into kafka.
- Then we will create airflow pipeline.
- Then we will create ml-flow and we will run spark streaming job.
- So here we will be getting the real time data, So our first purpose is to create the base model with some benchmark accuracy.
- And gradually we will be getting huge throughput data at real-time which will affect the accuracy.
- So we need to fine-tune the model at that time.
- Airflow will play the role to train the model.
- Here once airflow trains the model the data will be pushed to the ml-flow.
- We can determine the performance of the model using mlflow.
- So after each iteration if we are getting the performance improvement bump in the model then it is meaningful otherwise there is no such meaning of upgrading to the new model.
- So once we have a model that has a good performance so we can use that one in the pyspark to infer the newly comming data points.
- Here we will be running all the stuff in the local so we will be using single kafka topic to produce the data.
- But in the production we will have collection of kafka topics which produces the heavy range of the data.
- So we will build the system in such a way that only from 1-2 % transactions will be published as a fraudulent.
- Because if our system is identifying 10-20% fraudulent transactions then it is not the practical scenario. Then there is something wrong in the system itself.

## Machine Learning Model Features

- Real-Time data consumption from kafka
- Temporal and behavioural feature engineering
- Class imbalance handling with SMOTE
- Hyper paramenter tuning with RandomizedSearchCV
- XGBoost classifier with optimized threshold
- MLFlow experiment tracking and model registry
- Minio (s3) integration for model storage
- Comprehensive metrics and visualization logging
- 