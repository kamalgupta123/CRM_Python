myapp.tcs.com for email

from flask import render_template
import random
from .models import Quotes

from helloapp import app, db
import random

## Define below a view function 'hello', which displays the message 
## "Hello World!!! I've run my first Flask application."
## The view function 'hello' should be mapped to URL '/' .
## The view function must render the template 'index.html'
@app.route('/')
def hello():
  return "Hello World!!! I've run my first Flask application."

@app.route('/hello/<username>/')
def hello_user(username):
  quotes = [
    "Only two things are infinite, the universe and human stupidity, and I'm not sure about the former.",
    "Give me six hours to chop down a tree and I will spend the first four sharpening the axe.",
    "Tell me and I forget. Teach me and I remember. Involve me and I learn.",
    "Listen to many, speak to a few.",
    "Only when the tide goes out do you discover who has been swimming naked."
  ]
  random_quote = random.choice(quotes)

  return "<h2>Hello "+username+"</h2><h3>Quote of the Day for You</h3><p>"+random_quote+"</p>"

@app.route('/quotes/')
def display_quotes():
  quotes = [
    "Only two things are infinite, the universe and human stupidity, and I'm not sure about the former.",
    "Give me six hours to chop down a tree and I will spend the first four sharpening the axe.",
    "Tell me and I forget. Teach me and I remember. Involve me and I learn.",
    "Listen to many, speak to a few.",
    "Only when the tide goes out do you discover who's been swimming naked."
  ]
  html_string = "<h1>Famous Quotes</h1><ul>"
    
  for quote in quotes:
    html_string += "<li>"+quote+"</li>"
    
  html_string += "</ul>"

  return html_string

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000)


kubernetes - create cluster in cloud AWS using minikube command (docker cluster server) than in the cluster deploy application by running yaml file and creating pod (app) - yaml file create pod (app) in cluster


passcode - 5103296

TCS Outlook mail with GEHC
Work related message over teams
Any person from my team in noida v


Connect to India West VPN Gateway

iam WHICH USER HAVE ACCESS TO WHICH SERVICES

GROUP MULTIPLE USER IN GROUP TO ACCESS SERVICES

ec2 SERVER VIRTUAL MACHINE TO HOST WEBSITE

pRIVATE iP INSIDE NETWORK SAME FOR 2 NETWORK

elasTIC IP NOT CHANGING

efs EXTRA STORAGE HARD DISK with ec2

ami SHARED STORAGE MULTIPLE PC WITH EC2

LOAD BALANCER HEALTH CHECK API IF LOAD MORE ROUTE TO DIFFERENT EC2 INSTANCE

CREATE ANOTHER EC2 instance if load more health check api load balancer auto scaling automatically create another ec2 instance

Route 53 DNS provider map DOmain www.example.com to IP address of EC2 instance (Domain Registrar -- Route 53 ) A record to register IPV4 address and AAAA record to register IPV6 address EC2 instance

TTL time to live cache the domain with ec2 ip so no route53 more traffic for IP of ec2 access via domain through route53 A record cache it in browser for some time

Cloudwatch trigger alert for auto scaling when load increases on one server

CNAME in route53 for redirectring domain to some other domain pointing to an ec2 instance using alias

ROUTING POLICY TO ROUTE CLIENT REQUEST TO SERVER . DOMAIN TO IP OF EC2 ROUTE SIMPLE RANDOM ANY EC2 REQUEST GO ANY IP IN ROUTE53 added route in port 53

Weighted - specific weight added as per weight more preference to EC2 having more weight in route53

Latency - more closer EC2 instance area wise receive the request first

Health checks - to check if client domain is able to access EC2 instance lot many request further request failing security group deleted resource unhealthy

Failover - Don't go request to failed instance ip go to other ec2 ip if one fails

Geolocation - route as per location the request from which area that area ec2 route

Geoproximity - Biased more bias there go more traffic

IP based as per client IP check which EC2 instance mapped in table to that ip request go ROute53

Section cleanup - delete unnecessary instances to remove cost

Security group - allow These IPs to access the EC2 instance which IPs to access our EC2 instance

Policy - this json file these AWS services are allowed to be used in this policy

Virtual Private Cloud - these IPs are allowed to access the EC2 instance

Beanstalk - whole infrastructure of automatically create ec2 load balancers auto scaling other thinks PAAS deploy application directly cloudformation creates whole architechture EC2 others using flow chart

EFS and AMI are shared services for storage hard disks


Amazon S3 if large file upload then use multipart key of bucket 
s3:/bucket/folder_if_there/file_name.txt


S3 bucket policy - who can access the content inside bucket * means every user can access

to make website access by whole public not private use s3 bucket policy 

S3 storage can be used to host websites
upload all images on s3 storage make those images public using s3 bucket policy then upload index.html in static website hosting in s3 to make website

bucket will be accessible by object url

S3 versioning - new versions of uploaded file backup restore

one availability zone has different AWS service other availabilty zone has different service. for faster access to you country/continent availability zone select

S3 replication - whatever you upload in your current s3 bucket in one zone will automatically be uploaded to another s3 bucket in another zone if replication rule set in the first s3 bucket

different storage classes change of a s3 bucket for fast access, availability and durability.

lifecycle rules - 

transition to different storage class the s3 bucket based on need for faster access etc.

S3 Requester Pays - 
when someone s3 bucket accessed by someone else owner was paying previously now with this requester will pay

S3 Event Notifications -
whenever something inserted in S3 bucket notification is triggered as per event to different AWS services/SNS/SQS/Lambda and event access these services using policy so s3 has policy of lambda/SNS/SQS. that event goes if S3::putObject or S3::getObject 


S3:: faster upload and download file. upload file in parts (multipart) and fetch file in parts (some some bytes of file) -- S3 Byte Range Fetches

S3 select & Glacier Select - select the correct data from csv file uploaded in S3 bucket using Select query S3 query data from file uploaded in S3 server bucketr


S3 Batch Operations : operation on multiple s3 uploaded files together  move all files from one bucket to another

Encrypting all S3 objects/files together

retry if batch operation fail loggin notifications

Storage lens - metrics to optimize S3 storage export reports analysis to reduce cost and storage of S3

S3 select filter objects

CORS different domain access website from a different computer

MFA - to prevent login with malicious user on mobile and email OTP send multiple places for authentication login to S3
Presigned URLs - URL accessible from anywhere
Glacier vault lock - prevent S3 object from deletion lock them using policies
S3 Access Points - there are access points routes to securely access different folders inside bucket /analyse for analyse folder and /book to access book folder
S3 Object Lambda - for transformation of data fetched from S3 using lambda function code to modify the data
Cloud front - edge location nearby client user location where caching is done cache server is present there webpage comes from s3 bucket or public ec2 instance and cached in edge location for faster access of webpage next time this is cloud front

Allow list of countries to allow cloudfront caching of web page. Other countries not allow block caching at edge location
Cache invalidation - delete cache cloud front website CDN if any update made on website images or index.html of s3 static website hosting if updates not reflecting due to TTL of cache in cloudfront expire after 1 day then only latest come so delete the cache using cache invalidation to get latest website - cloudfront /images/* in s3 bucket inside images folder delete all images cache and /index.html delete index page cacheODP-Daas-BE/ibwingtowing (gehealthcare.com) - batch extract daas
 
https://github.gehealthcare.com/ODP-Daas-API/iscst-ibw2w - API
 ODP-Daas-BE/ibwingtowing (gehealthcare.com) - batch extract daas


RDS access requested
Tell Rajat for frontend access already raised RITM ticket send link
AWS access requested

dev-user for batch extract in AWS hc-daasbe-dev-user use to login in both dev(innovation evironment ) and prod environment use bolded user to login to AWS code we have raised request for AWS

AWS global accelerator - 2 EC2 instances inside 1 global accelerator closest EC2 instance region wise of your current location that EC2 instance if healthy access security group not deleted access the nearby ec2 instance using global accelerator

snow family ; offline data transfer in aws using storage medium like pendrives, external hard disks etc.


snow family se data s3 mein dalo to store data from s3 into glacier vault lock mein daalne k liye snow family ka data

amazon FSx - file explorer or file system to store files and folders like in windows file explorer fastly access file in persistent FSx backup of files created in FSx explorer also present backup in persistent

storage gateway - on premises locally and offline where client appication server or ec2 is present there is a cache storage offline storage connecting with gateway file from main server accessed will be present for some time in storage gateway as cache like in edge location for faster access.

Storage gateway -

cache based - for faster access some data come in gateway nearby server

on premises - for backup puprose offine take data in nearby hardware offline in gateway

AWS Transfer family - using TCP protocol transfer files and data to S3 bucket or seperate storage EFS and only authenticated users can access transfer family to transfer data to s3 bucket over TCP protocol's FTP file transfer protocol...put data to s3 using protocol making use of Transfer Family

AWS Data Sync - from offline server install software data sync connect with AWS and upload all data from offline hard disk computer to s3 bucket in AWS using Data Sync -- Data Sync functionality to transfer data to s3 from offline storage instead of offline transfer AWS to AWS also transfer.

EBS - extra storage to ec2 hard disk virtual of server

EFS - extra storage in multiple regions availability zones.

AMI - extra storage  shared by multiple EC2 instance

SQS - queue messages put in queue consumer take messages from queue and execute if queue between no direct communication between client and server its asynchronous lot many messages can go in queue by sender and lot many consumer can take 10 - 10 messages from queue and execute by consumer polling to check if there is any new message for him to execute


message in SQS queue go for processing to consumer for a visibility time period default v in second defined in AWS sqs queue if message not processed in that defined time it will again come back in queue from consumer and will be read by next consumer again 2nd time as it is not deleted/processed by 1 st consumer to delete/process the message of queue by 1st consumer you can increase the visibility default time period of queue from 30 s to 100s process and delete the message in that time span and next message will come in queue no same message will come to two different consumer if 1 delete/process the message by increasing visibility window


SQS Long Polling -

consumer can wait a lot much time to get his messages even if messages not in queue and come a little late so that no multiple request of poll is to be done by consumer in order to get message in single request he will wait for long time and get message no multiple request this will decrease latency

SQS FIFO Queues - 

order preserve these queue if message 1st come in queue 1st received by consumer 2nd message 2nd receive by consumer order preserve

SQS Queue - 

if lot many database inserts if direct communication if one insert not done some of them can be lost so Queue in between using auto scaling multiple consumer Ec2 and pick some some messages from queue different ec2 and store them in database 

no insert lost

all insert in queue one by one pick and insert in db only after 1st message insert then it is deleted from queue else not deleted so nothing lost

SQS can help in asynchronous processing in background use from frontend ec2 send mutiple processing task to queue another backend ec2 which can be auto scaled will pick the tasks from queue and execute in background.Single message publish to a topic all subscribes to topic on publish of message on that topic will receive that message automatically it is pub sub model for SMS email notifications and to other AWS services


With SNS SQS queue use multiple every SQS queue subscribed to topic so FIFO can be used for ordering after 1 processed then deleted no duplicacy in SNS message filtering if status = success publish message only success using filter policy and status = failure go to separate queue after getting filtered through filtering Policy in SNS


Kinesis Data Stream : data stream pipe to transfer data from one AWS service to another aws SERVICE  exaMPLE : LOGS OF EC2 INSTANCE FOR PROCESSING TO KINESIS LOG EXECUTOR 



AWS Certification student guide

https://login.us-east-1.auth.skillbuilder.aws/login?client_id=3dmkh0fidu87q7gjo0trgfj9d4&redirect_uri=https%3A%2F%2Fus-east-1.student.classrooms.aws.training%2Fcallback&response_type=code&scope=openid&state=c2efb9684f8742299cfe36b282da85a9&code_challenge=xrjaFugxjVCTuH6xKxh-v_osWlITmusFbB4-759scUg&code_challenge_method=S256&response_mode=query


Single message publish to a topic all subscribes to topic on publish of message on that topic will receive that message automatically it is pub sub model for SMS email notifications and to other AWS services

With SNS SQS queue use multiple every SQS queue subscribed to topic so FIFO can be used for ordering after 1 processed then deleted no duplicacy in SNS message filtering if status = success publish message only success using filter policy and status = failure go to separate queue after getting filtered through filtering Policy in SNS

Kinesis data stream push data in stream consume data from stream push data from one AWS service and consume in other use put product API of kinesis to put data in data stream in kinesis and get product API to create and iterator that will get the data and iterate over it. Get 10 10 items of data in each iteration then next ten like loop using iterator


Cloudfront TTL Edge Locations

Kinesis data firehose for data migration between AWS services buffer also there

AWS certification - google search

link -
https://aws.amazon.com/certification/certified-solutions-architect-associate/?ch=sec&sec=rmg&d=1

builder id - gupta.kamal1@tcs.com

SAA-C03 exam book

When take exam where take exam

In person pearson test center
AAdhar card and other things carry english

test center in my city take with date

Sample questions of AWS certification - 

Scenario based MCQ questions in examtopics

What asked in question 

more storage
less latency AWS exam certification

table chair and you no one else clean no surrounding neighbours and others

examtopics most voted would be the answer


AWS-ARC:  https://au1.qualtrics.com/jfe/form/SV_cAAOvXJ4f0ffSLj?atpclassid=159c4603-381d-4db6-a1e4-a514e1fea93e&Q_Language=EN

https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf

https://www.examtopics.com/exams/amazon/aws-certified-solutions-architect-associate-saa-c03

albin.thomas@trainocate.com -- for aws queries

KINESIS DATA FIREHOUSE HELPS IN DATA TRANSFORMATION WHILE TRANFERRING THROUGH DATA STREAM USING AWS LAMBDA

dATA IN KINESIS IS TRANSFERRED USING SHARDS TO KNOW WHICH SHARD THE DATA WILL GO TO THERE IS PARTITION KEY IN BUFFER LATER THE DATA IS TRANSFERRED TO ANOTHER AWS SERVICE FROM ONE AWS SERVICE USING KINESIS

Amazon MQ - like MQTT works in both offline and on AWS multi availability zone MQ for backup and failure handling copies of MQ in different availability zone Through EFS

DOcker - microservice multiple vitual machine ec2 create on single server using hypervisor in aws also docker container instead of ec2 multiple dockers for different microservices run on any O.S they have their own OS file then install python and run python app on docker

docker engine is there above EC2 which runs any container or pod of any programming language on EC2 as docker translates every programming language

Write once run anywhere docker 

DOCKER - MULTIPLE CONTAINER FOR DIFFERENT MICROSERVICE USING ONE IMAGE PYTHON DOCKER TO RUN PYTHON APP/MS

ECS AND EKS ARE USED TO CREATE MORE EC2 INSTANCES WHEN IN NEED MEANS AUTO SCALING DO INSIDE THE CLUSTER CREATE MORE INSTANCE IN EKS INSTANCE INSIDE CLUSTER KNOWN AS NODE AND CONTAINERS AS PODS

fARGATE IS SERVERLESS AWS AUTOMATICALLY CREATES EC2 FOR IT YOU DON'T NEED TO CREATE

tasks IN ECS IF NO DOCKER CONTAINER THAN TASK TO ACCESS AWS SERVICES NOT RUN APP APP ACCESS AWS SERVICES

aws APP RUNNER RUN APPS DIRECTLY EVERY EC2 VPC CREATED IN BACKEND AUTOMATICALLY

lambda is serverless (serverless means we do not have to create ec2 it would be automatically create by AWS) in lambda write code it will automatically pick s3 bucket and other AWS services

any programming language code write in lambda

lamba is event driven any event occur like s3 bucket file upload you can execute code on that event in any programming language without caring about creating ec2 instances in backend and linking with s3 services

autoscaling of lambda aws created ec2 instances if load more autoscaling

LIMIT (Numer of rows we want to skip, no of rows we need)

primary key unique
foreign key not unique

one to many ( many means not unique so foreign key in second table. first table primary key as foreign key in second table as foreign key not unique many side table

many to one foreign key in 1st table many side duplicates allow foreign key

lambda event from s3 automatically pick RDS database in python language lamdba script write event function of s3 and store file in RDS database 

clowatch ka ek tab aata hai lambda mein agar lambda function mein kahin bhi error aata hai you can check that error in cloudwatch tab or in cloudwatch logs

lambda snapstart take snapshot of lambda script initial startup phase .. 3 phases of lamda script running are there so next time lambda script runs it runs faster.

lambda function at edge location cloudfront run for faster access low latency to user similarly cloudfront functions to run at edge location with low latency to filter response and request for security things that at stored in cloudfront edge location as cache

As Lambda function is serverless it does not have VPC and EC2 it cannot access your VPC database so for serverless lambda to access your VPC database. you have to use Elastic Network Interface (ENI) and if multiple lambda access your vpc database if heavy load to distribute load used RDS Proxy to distribute load

from other services also you can execute lambda like data inseted in RDS database at that time trigger lamda data deleted take database snapshot send notification to sns after subscribing to events of eventbridge


Dynamo db service is fast noSQL add keyvalue pairs in dynamo db

Dynamo Db Accelerator (DAX) - Cache with dynamo db for faster access of data attach with database 

Dynamo DB stream processing - DB data streams from dynamo DB to push data from one table to another and process data also similar kinesis data stream take dynamo db data from stream to other AWS services S3

Dynamo DB GLobal Tables - Table accessible in multiple regions/locations for lower latency and backup of data

Dynamo DB TTL - TIme to live ... data in dynamo db live for that particular time as per TTL value.

Dynamo DB backups for disaster recovery

Put data from dynamo db to amazon s3 and analyse data in s3 using AWS athena

 API Gateway to create Rest  APIs serverless

HTTP endpoints GET POST with urls link to lambda function and data streams to s3 data put api gateway IAM role and policy to access API Gateway Authentication and other things done in api gateway

api gateway(API) link to lambda function

api gateway lamdba script error check in cloudwatch error logs tab

Step function : serverless workflow to create flow of lamda functions each step of the graph in case of success and failure what goes on next you can run other AWS services also in step functions

human approval feature also available in step functions


AWS cognito - users other than of AWS console ... third party mobile users access AWS services like Dynamo DB and RDS by verifying their third party users through cognito --- and then after verifying the third party user through cognito the user can access AWS services using API gateway load balancer through cognito pool or also directly through cognito identity


Third party user authenticated through cognito will access dynamo db as in dynamo db IAM policy cognito would me mentioned as user to access.

https://learning.oreilly.com/live-events/?page=1&sso_link=yes&sso_link_from=TCS

https://tcstop10.tcsapps.com/

S3 is key value store also as well as file store
DB graph social network --graph db - neptune
history store db encrypted -- qldb database
db to store timeline - timestram database
DB stream any insertion in DB move data from db to outside
NoSQL json db key-value - DynamoDB and DocumentDB

QLDB database - history of transactions all history store encrypted for blockchain also available

athena  --- all the s3 logs whenever s3 file was accessed all those logs are stored into s3 bucket using athena you can create a table of those logs by specifying the logs file bucket name so the table in athena will contain all s3 log file data as you have specified the logs file bucket name in CREATE DATABASE athen sql query so using log files bucket database and table of athena is created

Analyze s3 data -- athena

Athena for faster access -- partition logs data file data database data into seperate window using /column value or /data value in s3 url in athena to get particular url for faster access using glue convert data into column format to direct check column value and get data for faster access.

Redshift -- its OLAP analyse search some info from very big data not OLTP -- like mysql  --- in redshift its for data warehouse machine learning analyse it is faster because it searches on columns to get info query so it is fast. so there is columnar storage of data in redshift 10X more performance it provides -- parallel query engine

in redshift leader and compute node the sql query hits the leader node leader node checks the query and the access compute nodes to process the query and get the result data

provisioned redshift - create ec2 and VPC then create redshift cluster

Serverless redshift - AWS will itself create ec2 and VPC you do not have to create

In redshift for backup there are snapshot or Multi-AZ using multi AZ in different locations redshift cluster so backup copies of cluster data of redshift in multiple locations -- snapshot also move to a different Availability zone

To load data into redshift we have kinsesis firehose. kinesis firehose is a data stream to load large data into redshift

From S3 put data into redshift using copy command. or from ec2 to redshift using JDBC driver

Redshift spectrum -- data to query is present in s3 not in redshift so without loading data from s3 to redshift query the data through redshift spectrum interface which connects s3 and redshift cluster

Opensearch is like elastic search load the database data into it through kinesis or other data streams--- security credentials through cognito IAM...dashobards in opesearch to visualize opensearch data

Architechture -- integrate different AWS services together with open search dynamoDb data or cloudwatch logs 

AWS EMR - for big data many ec2 instances process large data it is faster processing service for big data provide apache spark for data analysis

different different ec2 if in demand we have to craete EMR for big data processsing use on demand instance .... if for 1 year EMR big data processing use for long running use reserved for cheap less used ec2 EMR use spot instances.

Quicksight : Integrate with large data store to analyse data and get buisness success insights from data used for data analysis...suppose Quicksight can integrate with redshift data store , RDS database or s3 and create dashboard to analyze buisness trends after generating the dashboard from quicksight you can send the dashboard to various users and group they can analyze the data using dashboard picture

Glue for ETL many diff services in glue that extract metadata of info along with information from data strores connected with glue and then later you can modify that data into some other format like s3 data using glue convert into parquet format (column format) to access data column wise for faster access.,.,..in amazon athena..so glue can extract and transform data different services in glue... there are data streams to fetch data from kinesis data streams...


Lake Formation - Data from multiple data stores like RDS, Redshift, S3 through data streams goes into data lake large data for machine learning and analytics the analysics can be done using AWS pyspark on top of data lake and then quicksight on top of AWS pyspark to visualize machine learning results of buisness insights --- using data lake all data come into one place so security apply in data lake only for users not in multiple places where data is coming from (data stores --redshift,rds) or going into (athena or quicksight) so not apply security at multiple places but in single place where data lake is present and all the data is present that is one benefit.

Kinesis Data analytics - through kinesis data stream put data from data stores to kinesis data analytics where using sql you can get required data then using data stream put data in lambda and analyze it .... Flink in kinesis data analytics to analyze lot of data and create backup (snapshots)


AWS MSK - Kafka - its also a data stream like kinesis load data from different data stroes into GLUE , ETL or lambda for large data analysis ...it is pub sub model and more data can be put into kafka the data in kaka is inserted from producer into channel then subscirbers scribed to topic will get data multiple subscribers can be there... (Migrate Kafka)

Data analysis -- Big Data

load data into s3 bucket using kinesis data streams and kinesis firehose then transform the data (columnar -- faster) using lambda query the data to get required information using Athena and visualize using quicksight -- AWS

AWS Rekognition - detect objects in videos...like which person what is written on whose shirt in video...ceo of tcs in video recognise and recognise which fruit in video.....also used to recognise criminal content in cideos like offensive and criminal images in website...in Amazon Reckognition AWS service you can do all this study video objects set a threshold if cross threshold flag item as criminal image should contain this this only

AWS Transcribe - convert voice to text tell anything to AWS it will write what you say in form of text and hide sensitive content.

use case : automatically create subtitles whatever it say..

sound..voice...speech convert to text.

amazon AWS Polly : convert text to speech...whatever write in polly convert into sounds...shortcuts write convert to full form sounds by adding key value pairs of short names with full forms in lexicons and using SAML longs <add break()> add break of 2 mintues in voice generated after full stop in text written or do other thing in text to generate different voice with break and other things programmatically.

AWS translate --- trqanslate website data from one language to another like english to spanish

LEx and Connect service in AWS : lex converts audio to text and connect helps to place calls. Using Lex one can create chatbot. in AWS so using AWS call via mobile (using connect) lex listens to call convert audio to text understand he want to schedule a meeting as per what said in call and schedules a meeting by using lambda in database (RDS) as per call audio analyze lex and lambda  

1265530@tcs.com

AWS Comprehend -- For natural language processing convert speech to text analyze when you are saying refers to which topic and whether you said negative or positive thing and others

AWS Comprehend Medical - Whatever 
data from audio using AWS transcribe convert into text and get medical insighsts from whole medical text whatever patients said about him important things get what medicine he takes how much dose and other things.

AWS SageMaker - for machine learning on AWS upload the dataset learn from data and predict about new data from previous employees resume score predict new employee score from his resume.

AWS Forecast - past dataset how much sales every year upload on S3 then learn from that dataset using AWS Forecast and predict next year (predict -- forecast) how much sale will be there in next year predict from past data using forecast

linux :

sudo su to run commands as admin
chmod to change file read write permissions
grep error/word filename - to search for errors and words in filename
search logs by going to particular directory

Cloud Practitioner:

multiple computer virtualisation as single computer (hypervisor) and provide ec2 in AWS in data centres multiple computers present

IAAS -- VPC EC2
PAAS - serverless no provision ec2 vpc -- lamdba elastic bean stalk
VPC - your private place create your own cloud application / infrastructure

S3 Lifecycle Rules - to move non frequently accessed file in S3 automatically to S3 Glacier using lifecycle rule not that much used big storage is glacier

Cloud computing is multiple computers are interconnected -- computer networks -- internet

AWS solution architect design optimal architechture for web app with faster using cache auto scaling and traffic distribute load balancer -- fast, less costly and reliable -- fault tolerant -- system architechture

Cloud Formation - template of code in coding language to create whole AWS architechture -- EC2 for web app and reuse that template from Cloud Formation to again recreate that architechture any time


AWS Quicksight -- dashboard to get buisness analysis how to make buisness successfull

minimum access provide to user as much he requires for security

IAM for security
Password login in website for security
API Keys secret id's to use AWS APIs for security
MFA receive text in code and email for security AWS
Redis Cache and Elastic cache lives on RAM that is why they are fast cache is closer to CPU as it is present in RAM not Hard disk

General Purpose EC2 -- everything medium medium -- fast, storage medium medium general not too fast not too much storage

Memory optimized EC2 - too much storage want

Compute Optimized EC2 - very fast EC2 want

Spot Instance  -- cheap ec2 instance want

AWS WAF - firewall to protect against DDOS security attacks and other cyber hacking hacks use this service for your website

AWS shield service - to protect against DDos Attacks

AWS Inspector - checks for security issues how website can be hacked and tells you those security issues

AWS Trusted advisor - tells what can be done to enhance website security, backup,fast (IAM, security groups) , backups - snapshots, authentication - (MFA)

AWS Guard Duty Service - 24/7 Machine Learning AI guard in AWS without sleep checks for any security threat or attack made on website and trigger cloudwatch alerts...it threat comes

AWS Billing - According to AWS service use its cost of service pay check cost of each service in AWS website

Free tier - everything is free upto limits GB of service use after GB over you have to pay

Developer Support Plan - Account in AWS - for developers you can get customer care support live chat and others in other support plan

There are services in AWS that can analyze your total cost billing of AWS infrastructure and using metrics tell you are where you can minimize cost of using AWS services



minimum priviliges give to users in website or AWS for security

AWS Solutions Architect - ML

AWS Kendra - Upload documents in AWS Kendra -- Kendra can learn from those documents word, pdf etc and provide answers.--using Machine Learning.

AWS Personalize -- In your AWS web app in order to provide recommendations based on what user search on the AWS website to user you can use AWS Personalize it learns from past user search data and provide recommendations

AWS textract - from any scanned document like passport pan card extract the passport and pan card user data through scanned copy intelligently using textract

Under Cloudwatch go to each service and you can see metrics/logs of that service...you can pass cloudwatch logs/metrics from kinesis data streams/firehose to other AWS services like to S3 and analyze the metrics in s3 using athena or analyze metrics using opensearch after passing metrics in opensearch through kinesis data stream.

zoom the metric graph using cut screenshot and check 5 5 pts

logs from different AWS services come into Cloudwatch logs then there is Cloudwatch logs Insights service to analyze cloudwatch logs by querying the logs as per timestamp to get logs of a duration or logs containing error or exception word put in query visualize also the logs after query in cloudwatch

from cloudwatch move logs to different AWS services using kinesis data stream and analyze

Cloud watch logs gp according to AWS service contains logs of that service inside them

search for error keyword or other keyword in search bar cloudwatch logs under gp to check for errors or something else  

log name - that_script_run_run_command_id/log_id/stdout_or_stderr

for error keyword in logs you can create custom metric to visualize how many error logs in graph form

create alar ion metric if metric if error logs goes above 2 -- more than 2 error trigger alarm in cloudwATCH

MOVE LOGS FROM CLOUDwatch to other AWS services.

You can set in how much time logs expire/get deleted

You can export logs to S3

Query cloudwatch logs you can see dummy queries of cloudwatch on the right hand side -- query logs of specific 

Query for data of logs for past hour -- also you can save and check dummy queries

metric - visualize (graphs)
logs - text data

AWS Live Tail - From log group get latest log in live tail last latest log get and see ...

CloudWatch Agent and Cloudwatch Logs Agent - It is installed on EC2's to transfer logs of EC2 from EC2 to cloudwatch to analyse

Cloudwatch Unified agent - Installed on EC2 to transfer logs as well as mETRICS OF ec2 TO CLOUDWATCH

Cloudwatch alarms: trigger notifications if data goes above the metric threshold limit so alarm montiors EC2 or other AWS services metrics status healthy unhealthy 

Cloudwatch alarms watch metrics -- to trigger alarms 


We can do operations like max min on metrrics or %age on metrics to trigger alarm

if data > max(10) -- (threshold) -- use min percentage also trigger alarm

Alarm has 3 states OK means alarm not triggered. Insufficient data means insufficient data to trigger alarm. and alarm means that threshold has been breached and notification will be sent.

Alarms can help in autoscaling of EC2..or stopping, terminating ot rebooting EC2...Alarm can help in sending notification to SNS from where we can trigger lambda from SNS based on alarm and can run any AWS service

There are composite alarms (AND and OR conditions (conjuction) use in two alarms) two or more alarms combine suppose one alarms trigger when CPU usage goes high > 90% and other alarm triggers when storage goes high > 100% and you want to trigger a composite alarm when both CPU and Storage goes high so you can use a and condition in the previous two alarm and can create a composite alarm which triggers when both CPU and Storage goes high.

Trigger alarms manually from command line AWS CLI or AWS console use trigger/set alarm command or api

create instance and search for the created instance id in cloudwatch alarms to create alarms for the instance using instance id in cloudwatch when CPU utilization goes > 90%

AWS Eventbridge : contains events from various AWS services. events are generated from different AWS services every hour. like EC2 iinstance when starts (event), stops(event)...craete cron jobs...events from all S3 bucket all AWS services every hour go to Eventbridge and those events can be filtered like i want to take event of only a particular S3 bucket out of all S3 bucket events...then after filter a jSON of filtered event you get from eventbridge... this json filtered event can help to trigeer other AWS services like lamdba () or EC2 instance start...

There is a event bus of eventbridge all events every hour sites in event bus

Custom event bus some particular AWS services you select will put events in that event bus

You can archive events from event bus and replay them and test for debugging

Eventbridge Analyze Json events came after filter in event bus and create schema...schema registry create code of event tell about event in event bus -- also you can get data about the event from that code in eventbridge

A specific event bus can be restricted to contain events from specific AWS serivce

Central Bus -- allow other accounts to send events to event bus using resource based policy 

React to an event and do something like IAM user login react to login event and trigger Email using SNS


Can create cron job -- run a lambda script function every hour

event archive to put event in archive and replay them retriggere event some time later

cross account access on event bus use resource based policy -- template load and you can edit it.

1. create an event bus
event comes from AWS services click on AWS service and set up up to trigger events in eventbridge

2. Create a rule like from which EC2 you want event which state stop , running or other state event trigger filter rule --- put filtered event in event bus -- sandbox to test filtered event on stopping is it getting triggered...

filtered rule event goes to selected event bus(default or newly created event bus)

default event bus contains all AWS services events but your created event bus has events from your particular setup AWS service

after event in event bus subscribe to those events using SNS topic for getting in other services like lambda to run code on it

schema if implement in code event structure what event contains data in python...event object get in python

Cloudwatch -- for logs of diff AWS services and metrics -- data graphs

Cloudwatch container insights : 
tell logs about containers to run different apps of python , java of EKS and ECS of AWS 

it tells logs of container since the cloudwatch container insights also run as container

Cloudwatch Lambda Insights:
CLoudwatch lambda insights tells logs about lambda script serverless written in any language python, java 

Cloudwatch Contributors insights :

In the whole web app or website running on AWS using different AWS services...Cloudwatch contributor insights tells logs about top 10 AWS services receiving highest traffic..top EC2's receiving highest traffic...it tells about top 10 things about any top 10 things other than traffic you want to know in the architechture

Cloudwatch Application Insights:

tells logs about the whole application having different AWS services so tell logs about those services used under the website or application running on AWS.


pan ADDRESS CHANGE GOVT WEBSITE :

https://www.pan.utiitsl.com/PAN_ONLINE/homeaddresschange

https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html

CloiudTrail Records events happened by which user or IAM user or which AWS service account details who switched off or terminated instance ... If Management Events AWS service modified IAM account Modified Data flow event reading and writing data to S3 store these events in cloudTrail to analyze who did it and for longer retention move to S3 and analyze with athena

CloudTrail EventBridge -

first delete api called to delete something in database. after the api is called the logs about it are captured in cloudwatch. after logs are captured in cloudwatch it can become an event in eventbrige select the delete data event of api through cloudwatch eventbrige whatever happens go in cloudwatch logs and then come in eventbridge. through eventbridge we cause use it as event whatever happened send that event to SNS and access other AWS services through SNS to trigger lambda or other services on that event.

AWS Config

It monitors and logs data about all Other AWS services...if they are compliant or not compliant as per rules defined in AWS config suppose a IAM user role is no longer needed as per AWS config it is non compliant it can be deleted and made compliant this action can be done using AWS config to make compliant this is called remediation so to delete IAM role it can be done using AWS lambda all the non compliant AWS services notifications are sent to AWS config using AWS config they can be modified or rectified to compliant using lambda and if any AWS service compliant notification can be sent to AWS config.

rules in AWS config select choose from dropdown to differentiate between compliant and non compliant aws resource/services

Organizational IAM account top level multiple account into one group put any rule allow to the group applied automatically to all other accounts in the group or organization sub organization can also be there if any rule applied to top organization the same rule then is applied to sub organization.

master account has child accounts

restrict some access for chil organization which are allowed in parent organization.

IAM conditions : In IAM policy we can create or write conditions to let only accounts present in the organization higher organizationa access the resource or restrict some account to not let access some AWS services/resources

IAM roles -- assume some other role take different permissions to access resource give up previous permission to access AWS resource/services. give up previous role and take new role / permissions -- IAM roles

IAM resource based policy - don't give up previous permissions take new permissions --- and access resource using new permission and access previous AWs services/resources also using old permissions.

IAM permission boundaries: Top level restriction only these these services IAM user can access not other set boundary if all 3 set Organization restriction sub organization and boundary also set and policy for restriction also set then common intersection of all these 3 permissions take.

AWS IAM Identity Center : Single SSO -- single sign on and access AWS services using single sign on as those users added with policies in identity center of AWS and access AWS cloud apps all using single sign on

AWS Directory Services - Microsoft Active Directory - Microsoft AD - sign on in master computer then all slave computer connected to master there also with same account can access access file system same in other computers also

AWS Control Tower : To secure not let all access AWS resource only these regions can be accessed.

Encryption :  
Client Side -- when in client side and on the channel packet is encrypted no One can take the packet in its way but in server side it comes and server cannot decrypt it only client can see so store and retrieve from server

Server side - no in client side not in channel only server can encrypt and decrypt packet exploited in channel no encryption trust server

Use together CLient side and server side -- 

client side when channel don't trust use man in the middle attack

server side when server trust

Server side

KMS (key Management System)- Store the encryption keys those keys in KMS can be accessed using KMS policies.

AWS managed keys - Keys created by aws stored in KMS(key Management System) aws prebuilt keys for encrypting AWS resource only with keys those AWS resource can be used like EC2, SNS etc

Customer Managed Keys - Keys that you yourself create to encrypt AWS resources like EC2 and SNS

Symmetric Key Algorithm - AES
Asymmetric Key Algorithm - RSA

Differentiation is opposite of Integration
Differentiation is large to small and Integration is small to large
by differentiation you can minimise error
because differentiation is for decreasing

linear algebra - vector -- values that specify something matrix
eigen vectors -- minimal vectors all other values calculated from this..

Probability - all sum 1
Probability Distribution - Sum of all probabilities is 1
Random Variables -- all outcomes of event you did every action you did its result
all the probabilities

probability distribution is showing all the probabilties of events in graph so all the training set with their outcomes shown in graph ... so if training set graph shows a prdefined probability distribution like bernoulli we can then apply algorithm to train that training set as per bernoulli distribution algorithm that we should use se thats how we come to know which algorithm best suite to train the training set to predict new things using probability.

P(A|B) - probability of event A or B how many times A happens or B event happens we can show this using Venn Diagram of Intersection both Common event A and B together How many times.

P(A|B) is not equal to P(B|A) this is Naive Baye's THeorem depend
if you know P(A|B) you can calculate probabiltity P(B|A) as both have A ∩ B in there as A∩B is what calculated in both as it is A or B so we get A∩B value from both and get naive baye's formula to calculate P(B|A) from P(A|B)

 

Statistics - see the data in graphs analyse it and deduce relationship in data..
also helps in data cleaning using normalization.

Statistics tells relationship between data
Mean - average rating
Median - middle value
Mode - most frequent - bought, seen, visited
Percentile - below that percent less many people many 90 below below you if you have 90 percentile
Range if lot many data to analyse put data in subgroups range
Discrete data - finite value 1 or 2 or 3 or 4
Continuous data - Infinite value group
Variance and standard deviation - it is how far a value is from mean is variance and farness is standard deviation for outliers
Missing data null fill with mean and median
Correlation , covariance and correlation coffecient - if one value increases other value also increases positive correlation or covariance or coefficient if one V increases other decrease negative correlation or covariance or coefficient
Probability distribution - binomial - 2 outcomes
Bernoulli - unlimited trials events of 2 outcomes event
Multimonial - multiple outcomes greater than six rolling a dice
Check distribution of graph graph see of training data and as per distribution apply ML algo
Not whole population survey do to collect data as population large whole can’t do take sample of population if one take from population do not remove that one from population and put in sample also this is non replacement and remove from population and put in sample is replacent - ways to create small sample spaces from population as getting data from whole population is tough
Linear regression line equation fit data predict next point decrease error of data by minimizing error by subtraction of mean or something


Computer Network:

Same subnet IP can communicate with each other different subnet IP cannot communicate should go through router 


Subnet mask 255 occupied IP 0 free available IPs:

255.255.255.0  --- 254 available IPs

Operating System:

Priority based process execute if one process important to execute in O.S give it priority

Round Robin - if one by one all process equal chance give.

Race condition -- multiple Threads or process execute same Resource 10 V variable 11 and 9 change wrong output provide use Lock variable if lock ==0 then only go to shared resource access if shared resource getting accessed put lock =1

if lock == 0:
   access shared resource
  inside code put lock = 1 code line update

if lock == 0 only access resource both processes.


Deadlock if cycle no one free resource

Deadlock Prevention code

IF resource free:
    Then only access resource

If resource.is_free():
   access_resource()

Fork:
A process copied from another process not created new process again if need to be accessed by multiple users same process again copied no need to create new process allocate new memory time waste using fork create copy make speedly

Multi threading no new process resource copy same resource share between multiple threads very very fast

You can store data in cache for faster access ...
programmatically also in python using @cache

also you can store data in registers .....

paging -- page

pages partition in memory so access the data in memeory using page no. and index no. index no. is the partition no. in page where data is stored.

LRU - least used page replace ..... by checking history so faster access by  checking history of least used page

AWS :
------
KMS store secret keys to encrypt important credentials. Only Users Account with access in KMS can access those keys.. you can provide access to some other account also to access those keys


Multi Region KMS Key Encrypt and Decrypt Data Anywhere in any AWS region.

AMI Image share for autoscaling creating new ec2 instances with other AWS IAM accounts along with KMS key to encrypt and unecrypt the AMI image using KEy while sharing from one account to another.

SSM : Like KMS store your secret keys here. these secret keys are encrypted and store in tree fashion hierarchy according to environment name dev or prod

Use TTL with secret key to expire credentials to not let necessary and important credentials get into hands of someone. --- send notification to eventbridge when parametre is deleted, created.

AWS Secret Manager - store db credentials , secret keys like in KMS and SSM and you can rotate the secret keys/ credentials and can change the credentials whenever you want you can refresh the credentials. YOu can put these credentials in multiple Availability zones....

AWS Certification exam important things :
-----------------------------------------------
Code of conduct read fast of exam attempt within 5 minutes else exam close
Don't move anywhere from camera while exam attempt
Take Aadhar ID with you on exam video
Contact Customer care in case of any problem like
Rechange profile information or account or test information through setting rechange re register acc
reschedule exam in case of exam end vouncher end date should still be valid using link account link
Final result of your certification test will come to your account check account after 5 days

If you fail an exam, you must wait 14 calendar days before you are eligible to retake the exam.

Once you have passed an exam, you will not be able to retake the same exam for two years. 

Certification verification
There are multiple ways that a certification can be verified:

Digital badge: You can download your digital badge, which can be used as a verification. Digital badges can be managed and shared under the Digital Badges tab in your AWS Certification Account.
Validation number: You can access your validation number from your AWS Certified PDF certificate found under Achieved Certifications in your AWS Certification Account. This 16-digit alphanumeric code can used to authenticate the credential by anyone with whom you have shared it with at the public URL http://aws.amazon.com/verification.Rescheduling and canceling


If you need to reschedule or cancel your exam, you can do so through your AWS Certification Account or by contacting Pearson VUE (Online Exam at Home) Customer Service. Be sure to reschedule or cancel at least 24 hoursWhen will I get my score report?

For both test center and OnVUE exams, most online results are available within five business days through your AWS Certification Account. AWS will email you when your results are ready to view online. If you pass your exam, you will also receive an email before your results are posted. For more information see the AWS website.


AWS Solutions Architect:

AWS Well Architected Framework :

Check the AWS Architechture you created in AWS console. and you can test the architechture if it is secure, fast, backup/reliable available by testing your aws architechture in Well Architechted Framework

AWS Certificate Manager:

Store TLS certificate new certificate for SSL or HTTPS create in website instead of SSL certificate now TLS AWS certificate Manager store TLS certificate when expire TLS certificate autorenew as event triggered through eventbridge on expire in AWS certificate manager ... To make website secure with HTTPS TLS Certificate Manager Sits in between as AWS service and other services

AWS WAF (Web Application Firewall) -

Rules rules written in access control list to protect your web application in AWS to protect against SQL Injection and cross side scripting

Apply WAF in load balancer with other AWS serivdes Like AWS certificate Manager to build whole architechture.

Egress only Internet gateway - private subnet ec2 contacted with Internet through NAT gateway in public subnet
Instead of NAT gateway in public subnet private subnet ec2 can contact directly to internet (internet gateway) using Egress only instead of NAT gateway directly through private subnet instead of public

Terminate running instance unnecessarily and remove and delete other things like VPC and subnet created as it will cost you money

All things like internet gateway internet and ec2 are connected using route table subnet created using CIDR subnet mask .. VPC flow logs to check attackers are attacking VPC or not

Egress traffic out not in

Ingress internet in not out

Security gp firewall for ec2
NACL firewall for subnet

Disaster Recovery : if electricity off system off backup in multiple availability zone put and for disaster recovery take snapshot backup copy

Database Migration tool  and schema conversion tool in AWS to convert MySQL to MongoDB by running a EC2 to convert in Database Migration service

AWS Backup service - select services in AWS like EC2 in AWS Backup its data will be automatically backed up in ec2. Also AWS Backup service vault lock to prevent malicious delete of backups

AWS application discovery service - for backup see which service to select in AWS backup which data is mapped to which service data which service and data to select for taking backup….check mapping with this service
VMware service to run in offline on premise server setup run AWS cloud services

SQS queue FIFO prevents data loss process data one by one other wait … fan out pattern
To send data from s3 service to lambda to process use sNS subscribe to SNS topic all 3 Or multiple SQS queue data published to SNS topic via S3 when put or get object transferred copies of same data to all SQS queue as they have subscribed to the topic… same copy transferred to all SQS as subscribed to SNS topic

Complex  RDS SQL queries cache using memcache, Redis and DAX part of elastic cache

Blocking IP address in net
To block IP address in VPC use NACL to disallow IP address
Inside VPC in EC2 security group only allow is there in security group no deny so only allow non malicious IP that you want to allow
Also you can use firewall in EC2
WAF to block IP
Cloudfront geo restriction to block IP

Cloud formation : whole AWS architechture/ infrastructure tell to create via code … it saves cost and you can view the architechture created via code via Template whole flow chart using AWS application composer template see

Define IAM role for cloudformation take IAM permission to create architechture via code

AWS SES - to send email via AWS

Amazon pinpoint - CRM to send advertisement to customers via SMS, email other activities

AWS session Manager : ssh to ec2 securely connect to ec2 securely there are IAM permissions

AWS systems manager run a single command to multiple ec2 for updating/patching multiple ec2 at once output of command for update put in cloud watch logs

AWS cost explorer : how much cost of AWs sevices forecast from previous services ec2 usage per hour

AWS cost anamoly service : using Machine learning detect where cost is more in AWS architechture

AWS outposts - hybrid cloud on premise offline and AWS using outposts create on premise offline architechture in AWS hybrid cloud make

AWS AppFlow : transfer SAAS software as a service like service now and sap data to aws

AwS amplify : provide all AWS services in one place to create web and mobile apps

AWS instance scheduler : Works with cloud formation whole infrastructure created with cloudformation instance scheduler checks with AWS services to start and stop to minimize cost of architechture created with cloudformation.

AWS batch : unlike lambda not serverless no time limit run job and create unlimited amount of ec2 to successfully finish the job/ script how large script

AWS trusted advisor : give suggestions on AWS services what to modify to increase performance.
