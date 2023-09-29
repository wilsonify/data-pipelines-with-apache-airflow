# Chapter 1

Code accompanying Chapter 1 of the book 'Data pipelines with Apache Airflow'.

## Contents

This code example contains the following DAGs:

- 01_umbrella_predictions.py - DAG illustrating the Umbrella use case.

```mermaid
graph LR
    A1["Fetch Weather Forecast"] --> B1["Clean Weather Data"] --> C1["Push Weather to Dashboard"]
    A2["Fetch Sales Forecast"] --> B2["Clean Sales Data"] --> C2["Push Sales to Dashboard"]
```

```mermaid
graph LR
    weather("weather API") -- Fetch --> combine["join datasets"] 
    sales("sales data") -- Fetch --> combine
    combine --> train --> predict
```

## Usage

To get started with the code examples, start Airflow in docker using the following command:

    docker-compose up -d

Wait for a few seconds and 
you should be able to access the examples at http://localhost:8080

To stop running the examples, run the following command:

    docker-compose down


```mermaid
graph LR
    subgraph scheduler
        read[read DAG] --> check[check schedule]--> dependencies[check dependencies] --> add["add tasks to queue"] 
        add --> wait --> check 
    end

    users -- monitor --> webserver -- store results --> database 
    users -- write --> DAGs -- describe --> pipelines
    DAGs -- read by --> scheduler
    scheduler -- schedules tasks --> Queue 
    scheduler -- serialize --> database 
    Queue  -- executes tasks --> workers
```

Data pipelines can be represented as DAGs, 
which clearly define tasks and their dependencies. 

These graphs can be executed efficiently, 
taking advantage of any parallelism inherent in the dependency structure.

Although many workflow managers have been developed over the years for executing graphs of tasks, 
Airflow has several key features that makes it uniquely suited for implementing efficient, 
batch-oriented data pipelines.

Airflow consists of three core components: 
* the webserver 
* the scheduler 
* the worker  

They work together to schedule tasks from your data
pipelines and help you monitor their results.