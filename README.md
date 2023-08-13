# Architecture 

| __lambda name__ | __purpose__                                                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------------------------ |
| gatherer        | downloads data from ffiec. unzips it. preliminary data clean. uploads folders to s3. only one of these will exist. |
| processor       | downloads specific folder from s3. cleans data. uploads it to RDS. many of these will be spun up; 1 per folder.    |

## Questions for Jae
* how can I get AWS credentials to the account?
* what are the naming conventions for tables in the RDS?
	* this will dictate what metadata we need to preserve

---
# Stories
## TODO
- [x] [[#Scaffold Repository]]
- [ ] [[#Dockerize and extend functionality for GATHERER lambda]]
- [ ] [[#Dockerize and extend functionality for PROCESSOR lambda]]
- [ ] [[#Consider how to handle multiple lambdas uploading to RDS at one time]]

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

### Dockerize and extend functionality for GATHERER lambda

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
