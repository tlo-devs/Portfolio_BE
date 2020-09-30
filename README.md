# Portfolio Backend

This project contains the Backend and
Admin panel for the 11SevenDome Portfolio
Website.  

## Clone for local development

1. Clone Repository

2. Add keys folder at project root

3. Add storage_ops.json auth
file for GCP in the keys folder

4. Add file named keys.py inside of the
settings module, containing the
follwing variables:
    - SECRET_KEY: str
    - PAYPAL_CLIENT: str
    - PAYPAL_SECRET: str
    - PAYPAL_SANDBOX: bool
    - CLOUD_SQL_CONN_NAME: str

5. Add file named prod_admin.py inside of
the settings module, containing the
following variables:  
    - PROD_ADMIN_EMAIL: str
    - PROD_ADMIN_PASSWORD: str

5. Add terraform.tfvars in the
.terraform folder, containing the
following variables:
    - db_password: str
    - db_username: str
    - db_name: str

6. Run the included docker-compose file,
located under /docker/docker-compose.yml
by running:  
``docker-compose up --build -f docker/docker-compose.yml``  
Remember to adjust the paths to your OS  

The application should now be available at
localhost:8001.  
The OpenAPI docs can be found at /redoc

For notes on the deployment process,
refer to the README in the .terraform
directory of this repository.
