## Running the Deployment

As a thing to keep in mind:
The state of this deployment is stored
locally, as such all attempted deployments
should be discussed first.  

Remember to adjust the credentials path.

Initialize Terraform:  
``terraform init``

Make sure everything is in order:  
``terraform plan``

Deploy:  
``terraform deploy``

### Notes

Deployment region will be eu-central-4 as
CloudRun does not yet support eu-central-3.  

### Excluded resources

- CloudRun container
