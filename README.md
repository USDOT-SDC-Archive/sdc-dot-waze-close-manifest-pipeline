[![Build Status](https://travis-ci.org/usdot-jpo-sdc-projects/sdc-dot-waze-close-manifest-pipeline.svg?branch=develop)](https://travis-ci.org/usdot-jpo-sdc-projects/sdc-dot-waze-close-manifest-pipeline)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=usdot-jpo-sdc-projects_sdc-dot-waze-close-manifest-pipeline&metric=coverage)](https://sonarcloud.io/dashboard?id=usdot-jpo-sdc-projects_sdc-dot-waze-close-manifest-pipeline)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=usdot-jpo-sdc-projects_sdc-dot-waze-close-manifest-pipeline&metric=alert_status)](https://sonarcloud.io/dashboard?id=usdot-jpo-sdc-projects_sdc-dot-waze-close-manifest-pipeline)
# sdc-dot-waze-close-manifest-pipeline
This lambda function is responsible for deleting the message from the queue and send a notification to the SNS topic for the completion of the manifest generation.

<a name="toc"/>
## Table of Contents

[I. Release Notes](#release-notes)

[II. Overview](#overview)

[III. Design Diagram](#design-diagram)

[IV. Getting Started](#getting-started)

[V. Unit Tests](#unit-tests)

[VI. Support](#support)

---

<a name="release-notes"/>


## [I. Release Notes](ReleaseNotes.md)
TO BE UPDATED

<a name="overview"/>

## II. Overview

There are two primary functions that this lambda function serves:
* **delete_sqs_message** - deletes message in the queue for which the manifest generation has completed.
* **publish_message_to_sns** - publishes the message to the SNS topic indicating that the manifest generation has completed for a particular batch Id.

<a name="design-diagram"/>

## III. Design Diagram

![sdc-dot-poll-for-batches-to-manifest](images/manifest-generation.png)

<a name="getting-started"/>

## IV. Getting Started

The following instructions describe the procedure to build and deploy the lambda.

### Prerequisites
* NA 

---
### ThirdParty library

*NA

### Licensed softwares

*NA

### Programming tool versions

*Python 3.6


---
### Build and Deploy the Lambda

#### Environment Variables
Below are the environment variable needed :- 

BATCH_NOTIFICATION_SNS - {arn_of_the_sns_topic_to_send_the_notification}

manifest_sqs  - {name_of_the_sqs_fifo_queue_to_poll_messages_from}

#### Build Process

**Step 1**: Setup virtual environment on your system by foloowing below link
https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html#with-s3-example-deployment-pkg-python

**Step 2**: Create a script with below contents e.g(sdc-dot-waze-close-manifest-pipeline.sh)
```#!/bin/sh

cd sdc-dot-waze-close-manifest-pipeline
zipFileName="sdc-dot-waze-close-manifest-pipeline.zip"

zip -r9 $zipFileName common/*
zip -r9 $zipFileName lambdas/*
zip -r9 $zipFileName README.md
zip -r9 $zipFileName persistence_close_statemachine_handler_main.py
zip -r9 $zipFileName root.py
```

**Step 3**: Change the permission of the script file

```
chmod u+x sdc-dot-waze-close-manifest-pipeline.sh
```

**Step 4** Run the script file
./sdc-dot-waze-close-manifest-pipeline.sh

**Step 5**: Upload the sdc-dot-waze-close-manifest-pipeline.zip generated from Step 4 to a lambda function via aws console.

[Back to top](#toc)

---
<a name="unit-tests"/>

## V. Unit Tests

TO BE UPDATED

---
<a name="support"/>

## VI. Support

For any queries you can reach to support@securedatacommons.com
---
[Back to top](#toc)
