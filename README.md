# CloudGuruChallenge - Event-Driven Python on AWS



[![Actions Status](https://github.com/ashokballolli/acg-etl/workflows/Terraform/badge.svg)](https://github.com/ashokballolli/acg-etl/actions)

I came across #CloudGuruChallenge through one of my LinkedIn connections. The challenge is to create an event-driven ETL processing pipeline for COVID-19 data using python and AWS services.
Below I'll explain how I worked through each step of the challenge, so let's get started.
  - Challenge Details can be found [here](https://acloudguru.com/blog/engineering/cloudguruchallenge-python-aws-etl).
  - Access the dashboard [here](https://app.redash.io/ashokballolli/public/dashboards/nmuwU70jPpuT3gG8mZmhEdl2NLE3LXxi0NqQqM9s?p_Date%20Range=2020-01-22--2020-10-31).

## Architecture diagram:

![](https://github.com/ashokballolli/acg-etl/blob/master/readme_images/acg-etl-architecture.png?raw=true)

## Extract, transform and load:
*  Extraction: 
Downloaded the two CSV files from different urls(New York Times and John Hopkins Github sources) and read them as python's pandas dataframes.

*  Transformation: 
In the transformation layer, converted the column string date into date object and deaths, cases, recovered columns into integers. Filtered the dataframes only for US data and kept only those columns which are required(date, cases, deaths, recovered). Merged two data sets into one.
*  Load: 
Transformed and well formatted data which is returned by above transformation module is then loaded into a PostgreSQL RDS instance using python's psycopg2 library. And here the logic also includes to insert all the data if the ETL is running for the very first time and to consider only the delta for any of the next ETL runs. 

### Alerts:
The ETL also triggers the SNS email notification to the subscribed email id's with the number of new records loaded into table in case of success and error details in case of any failure/error/exception.
### Tests: 
Used the testing.postgresql library which setups a postgresql instance in a temporary directory, and destroys it after testing, used unittest which is python's unit testing framework and kept static test data files to simulate the required test scenarios. The repository includes 16 tests to cover most of the ETL functionality.
## IaC using Terraform:
This was the best part of this challenge, got to learn a lot. I never worked with AWS CloudFormation or Terraform before, after a bit of research decided to go with terraform because of the community support, best documentation and materials to learn and terraform supports all the major cloud service providers and also 3rd party services. 
The infrastructure is completely automated using terraform. It includes provisioning the services, setting up roles, establishing the connection between different services, updating the latest code to the lambda function and lambda layer.
Same is also integrated with the CI/CD pipeline which will update the infrastructure as needed when any code changes are pushed to the code repository.

Yes, now I am a big fan of terraform, which really eliminates the probability of error, provides high reusability and portability and saves lot of time in creating and destroying the complex infrastructure.
## CI/CD Pipeline: 
I used Jenkins a lot in the past but never used github actions. So decided to explore and learn github actions this time. 
Github actions will be triggered as and when code is pushed to the repository. Here I have configured 2 jobs,
  - Build and run the tests.
  - If the step-1 is success and all the tests pass then it triggers terraform code to create/update the infrastructure and deploy the latest code and libraries to S3 and sync to lambda function and lambda layer.

Used github secrets to store the sensitive data and which is passed as environment variables to the terraform code.
## Dashboard: 
Data isn't meaningful without the report and a way to visualize it. Started with QuickSight which I never used before, and able to build the first version of dashboard. But because of QuickSight's restrictions to expose it to public and some of the limitations while building the report, I decided to switch to another open source tool "redash". Referred some youtube videos and was able to setup the dashboard.
The dashboard is currently configured to refresh every hour.
![](https://github.com/ashokballolli/acg-etl/blob/master/readme_images/covid-dashboard.png?raw=true)

## Challenges and Learnings:
  - Lambda: As I have started using Lambda with just some theoretical knowledge, struggled to figure out the reason for lambda errors with the libraries. The libraries downloaded on my mac didn't work in lambda, currently the github actions+terraform runs it on ubuntu and uploads.
  - Size restrictions on lambda layer: Initially started with uploading the zipped libraries manually directly to the lambda layer and attached it to the lambda function. Later when this zipped file size increased to >50MB, changed the storage of this file and also the zipped code to S3. Currently the github actions+terraform takes care of downloading, zipping, uploading to S3 and attaching them to lambda layer and function.
  - Terraform: Terraform currently doesn't support the email as SNS subscription protocol, because the endpoint needs to be authorized and does not generate an ARN until the target email address has been validated and this breaks the Terraform model. This is resolved by calling the CloudFormation i.e. Our terraform module runs a CloudFormation template that will provide us with the ability to bring email support. Reference
  - Struggled a bit to establish dependency while running the github actions. Able to make the tests success criteria as dependency to trigger the terraform code and 'terraform apply' only if changes detected in 'terraform plan'.
  - It took more time than expected in making terraform code modularised. Currently, the root terraform orchestrates all the modules, adds dependency between modules, passes the output variables from one module to another(ex: passing the rds database hostname, dbname from rds module to lambda function).

## Conclusion:
This challenge enabled me to perform hands on integration of multiples AWS services. Learnt to use github actions and terraform, will be exploring more on them. Learnt how to work with lambda functions and layers. A big shout out to Forrest Brazeal for creating this challenge. Looking forward to more challenges from "A Cloud Guru".
It was great learning experience and I would really appreciate any feedback or comments regarding the approach and the blog.
