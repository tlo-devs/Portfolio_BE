# Deployment

Deployment region will be eu-central-4 as
CloudRun does not yet support eu-central-3. 

As a thing to keep in mind:
The state of this deployment is stored
locally, as such all attempted deployments
should be discussed first.  

Remember to adjust the credentials path in
the .terraform/main.tf directory.

### Terraform excluded Resources

- CloudRun Container (Frontend)
- AppEngine Project (Backend)

## Prerequisites

- CloudSQL Admin API activated
- AppEngine Admin API activated
- CloudStorage API activated
- CloudBuild API activated
- CloudRun API activated
- CloudBuild ervice account has access
to CloudStorage
- exodia.json and storage_ops.json in
keys directory

## Flow

1. Provision infrastructure using
Terraform

2. Update Database connection string in
keys.py based on the exports from
infrastructure provisioning

3. Deploy to AppEngine using gcloud CLI

4. Link database to AppEngine project

5. Change AppEngine domain mapping

6. (Deploy Frontend)

### Provision using Terraform

While inside of this directory, do:  
``terraform init``  
``terraform fmt``  
``terraform plan -out="./terraform.plan"``  
``terraform apply "./terraform.plan"``  

To show current config:  
``terraform show``

To delete:  
``terraform destroy``

### Deploy to AppEngine

For this simply run:  
``bash gae-deploy.sh``
