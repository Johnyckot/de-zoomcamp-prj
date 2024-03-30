1. gsutil
2. docker
3. docker-compose
4. terraform

-------
Setup Teraform: 
    create a service account for terraform with roles:
    --service account admin
    save json file to ../keys/terraform-creds.json

Run terraform init, apply
Resources created:
    --todo describe resources (Q dataset, bucket, DataProc cluster)

for dataproc:
    region subnet of Default network should have Private Google Access = ON. Not clear how to set it in TF, since it was not created by TF
    the Service account which is used by DataProc VM should have access to GCS (e.g. Storage Admin). I used SA, which was created together with working VM and 
    manually granted the Role
------------

Start mage:
--todo: create bash script for Mage startup
 cd mage
 docker-compose build 
 docker-compose up
 
run Mage : http://localhost:6789/ 


