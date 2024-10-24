# Idle EC2 Instance Detection and Shutdown

## Overview
This project provides an automated solution to detect and stop idle EC2 instances in an AWS environment to optimize cost. It leverages AWS Lambda, CloudWatch, EC2 API, and SNS to monitor CPU utilization of running EC2 instances and stop or terminate instances that remain underutilized for a specified duration.

## Key Features:
- **Idle Detection**: Monitors EC2 instances' CPU utilization and marks those with low usage as idle.
- **Automatic Shutdown**: Stops idle instances after detecting prolonged inactivity.
- **Notification System**: Sends notifications via SNS when instances are stopped.

## AWS Services Used:
- **AWS Lambda**: Automates the instance monitoring and stopping process.
- **Amazon CloudWatch**: Monitors CPU utilization metrics.
- **Amazon SNS**: Sends notifications when instances are stopped.
- **Amazon EC2**: The instances being monitored and managed.

## Architecture

The solution consists of the following:
- **AWS Lambda** to run the logic that checks CPU utilization using CloudWatch metrics.
- **Amazon CloudWatch** to monitor CPU and network utilization.
- **Amazon SNS** to notify administrators when idle instances are stopped.

## Setup Instructions

### Step 1: Lambda Function Setup
1. **Create a Lambda Function**:
   - Go to the AWS Lambda console and create a new function.
   - Upload the `lambda_function.py` code to the Lambda function.

2. **Environment Variables**:
   - Add the following environment variable:
     - `SNS_TOPIC_ARN`: The ARN of the SNS topic for notifications.

3. **Add Permissions**:
   - Attach the appropriate IAM role to allow Lambda to describe EC2 instances, fetch CloudWatch metrics, stop instances, and publish to SNS.

### Step 2: CloudWatch Alarms Setup
1. Set up CloudWatch metrics for **CPUUtilization** for your running instances.
2. This is done automatically by the Lambda function, but you can monitor these manually as well if needed.

### Step 3: SNS Setup
1. **Create an SNS Topic**:
   - Go to the SNS console and create a new topic.
   - Add email or SMS subscriptions to receive real-time alerts when instances are stopped.

### Step 4: Test the Setup
1. Ensure that you have running instances in your AWS account.
2. Invoke the Lambda function manually or set it to trigger at regular intervals (using a CloudWatch event rule).
3. Check CloudWatch logs and SNS for notifications.

## Code Explanation

### lambda_function.py
This file contains the Lambda function code that:
- Describes running EC2 instances.
- Retrieves CPU utilization for the past hour using CloudWatch metrics.
- Stops instances where CPU usage has been below 5% for more than 1 hour.
- Sends notifications via SNS.

## Contributing
Feel free to contribute by opening issues or submitting pull requests. For major changes, please open an issue first to discuss the changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
