## Questions 
* how can I get AWS credentials to the account?
* what are the naming conventions for tables in the RDS?
	* this will dictate what metadata we need to preserve

---
# Stories
## TODO

- [x] Scaffold Repository
- [x] Create quarter_request_generator lambda
- [ ] Dockerize and extend functionality for quarter_data_collector lambda
- [ ] Dockerize and extend functionality for PROCESSOR lambda
- [ ] Consider how to handle multiple lambdas uploading to RDS at one time

## Leave for Team
- [ ] upload to database
- [ ] make this process a cron job

---

### Scaffold Repository
##### todo
* initialize a cdk project
	* create AWS gateway rest API
	* create an s3 bucket to store the files
	* create lambda
* ~~setup GitHub action to deploy infra on push to branch~~

##### requirements
* be able to deploy a hello world lambda
	* the lambda code should be __containerized__

---
### Create quarter_request_generator lambda

##### function
* given an input of start_year, start_quarter, end_year, end_quarter, generate a list. this list contains the offset number of quarters. for example, 2023 quarter 1 was 2 quarters ago. so it's offset would be -2.
* for each offset in the list, invoke the quarter_data_collector lambda

##### infrastructure
* build a skeleton for quarter_data_collector lambda
* give quarter_request_generator permission to invoke it.

##### requirements
* verify the quarter_request_generator can invoke the quarter_data_collector lambda.


### Dockerize and extend functionality for quarter_data_collector lambda

##### function
* wrap selenium functionality into a python docker lambda image
	* download the data
* use a multi core lambda to split up the work for parallelization
	* unzip the folder
		* create a folder in s3
			* __name it well__. that way we can use foldername as metadata so we know which table to put it in.
		* upload each file to s3, with async boto3 client.
##### infrastructure
* will need to grant policies / permissions to lambda to write to s3 bucket

##### requirements
* test the function manually to verify it is capable of uploading the content to s3.

---

### Dockerize and extend functionality for PROCESSOR lambda
1 function will be spun up for each folder that is uploaded to s3. So this lambda deals with things on a __folder basis__. The lambda will be triggered by API call.

##### function
* use async boto3 client to download the files to lambda
* use the existing cleaning functionality from old [repo](https://github.com/jacob-danner/db_scrape_automation)
* once in dataframes, should be easy to upload to RDS
	* __THIS WILL BE LEFT FOR THE TEAM__

##### infrastructure
* create a dockerfile that enables the needed libraries to be used
* connect the Gatherer lambda to the Processor lambda
	* Gatherer needs to be updated to send an API call once all files in a given folder has been uploaded.

##### requirements
* test the function manually to verify that it

---

### Consider how to handle multiple lambdas uploading to RDS at one time
* idk, to be determined.
