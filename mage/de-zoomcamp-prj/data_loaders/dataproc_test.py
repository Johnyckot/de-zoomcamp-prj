if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def start_cluster(cluster_client,project_id,region,cluster_name):
    print('Starting cluster...')
    operation = cluster_client.start_cluster(
    request={"project_id": project_id, "region": region, "cluster_name": cluster_name}
    )        
    # print(operation.result())

def stop_cluster(cluster_client,project_id,region,cluster_name):
    print('Stopping cluster...')
    operation = cluster_client.stop_cluster(
    request={"project_id": project_id, "region": region, "cluster_name": cluster_name}
    )        
    # print(operation.result())

def is_running_cluster(cluster_client,project_id,region,cluster_name):
    cluster_request = cluster_client.get_cluster(
    request={"project_id": project_id, "region": region, "cluster_name": cluster_name}
    )
    return cluster_request.status.state == 2    

@data_loader
def load_data(*args, **kwargs):
    from google.cloud import dataproc_v1 as dataproc   
    import time
    import os

    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/keys/mage-runner-creds.json"

    # input_path = 'gs://de-zoomcamp-shamdzmi-bucket/data/raw/2024-03-27/*.json.gz'
    # output_path = 'gs://de-zoomcamp-shamdzmi-bucket/data/stage/2024-03-27/'

    # gs://de-zoomcamp-shamdzmi-bucket/Code/githunb_transform_raw_stage.py
    # --input_path=gs://de-zoomcamp-shamdzmi-bucket/data/raw/2024-03-27/*.json.gz
    # --output_path=gs://de-zoomcamp-shamdzmi-bucket/data/stage/2024-03-27/


    cluster_client = dataproc.ClusterControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format('europe-west1')
    })

    # Define your cluster details
    project_id = 'de-zoomcamp-shamdzmi'
    region = 'europe-west1'
    cluster_name = 'dpc-zoomcamp'
    flag_stop_cluster=True 
    pyspark_file = 'gs://de-zoomcamp-shamdzmi-bucket/Code/githunb_transform_raw_stage.py'


    #Check the state of the Dataproc cluster and Start if not running
    if not is_running_cluster(cluster_client,project_id,region,cluster_name):
        print('Cluster is not in a Running state')
        start_cluster(cluster_client,project_id,region,cluster_name)

        # Initialize a Dataproc instance
    client = dataproc.JobControllerClient(client_options={
        'api_endpoint': '{}-dataproc.googleapis.com:443'.format('europe-west1')
    }) 


    # Prepare  pyspark job details
    job_payload = {
        'placement': {
            'cluster_name': cluster_name
        },
        'pyspark_job': {
            'main_python_file_uri': pyspark_file,
            "args":[
                "--input_path=gs://de-zoomcamp-shamdzmi-bucket/data/raw/2024-03-27/*.json.gz",
                "--output_path=gs://de-zoomcamp-shamdzmi-bucket/data/stage/2024-03-27/"
            ]
        }
    }

    # "pysparkJob": {
    #   "mainPythonFileUri": "gs://de-zoomcamp-shamdzmi-bucket/Code/githunb_transform_raw_stage.py",
    #   "properties": {},
    #   "args": [
    #     "--sd=aa"
    #   ]
    # }

    # Submit the job
    job_response = client.submit_job(project_id=project_id, region=region, job=job_payload)

    # Output a response
    print('Submitted job ID {}'.format(job_response.reference.job_id))
   
    job_id = job_response.reference.job_id
    job_info = client.get_job(project_id=project_id, region=region, job_id = job_id)
    is_done = job_info.done
    state =  job_info.status.state
    while not is_done:
        time.sleep(3)
        job_info = client.get_job(project_id=project_id, region=region, job_id = job_id)
        state =  job_info.status.state
        is_done = job_info.done
        print(f"Job state: {state} , is_done = {is_done}")

    
    #  if the flag is set then stop Dataproc cluster
    if flag_stop_cluster:
        stop_cluster(cluster_client,project_id,region,cluster_name)
    
    return state




@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert output == 5, 'Job failed, pls check logs in DataProc'
