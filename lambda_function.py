import boto3
import os
from datetime import datetime, timedelta

# Initialize boto3 clients for EC2, CloudWatch, and SNS
ec2_client = boto3.client('ec2')
cloudwatch_client = boto3.client('cloudwatch')
sns_client = boto3.client('sns')

# Get SNS topic ARN from environment variable
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')

# CPU utilization threshold and idle duration
CPU_THRESHOLD = 5  # CPU utilization below this value is considered idle
IDLE_DURATION_HOURS = 1  # Duration to consider instance idle (in hours)

def lambda_handler(event, context):
    # Get the current time and time one hour ago
    now = datetime.utcnow()
    start_time = now - timedelta(hours=IDLE_DURATION_HOURS)

    # Describe running EC2 instances
    response = ec2_client.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    
    idle_instances = []

    # Iterate through instances and gather CPU usage data
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']

            # Fetch CPU utilization from CloudWatch
            cpu_metric = cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=now,
                Period=3600,  # 1 hour period
                Statistics=['Average']
            )
            
            # Ensure datapoints are available for CPU usage
            if cpu_metric['Datapoints']:
                avg_cpu = cpu_metric['Datapoints'][0]['Average']
                print(f"Instance {instance_id} - Avg CPU: {avg_cpu}%")

                # Mark instance as idle if CPU is below the threshold
                if avg_cpu < CPU_THRESHOLD:
                    idle_instances.append(instance_id)
            else:
                print(f"No CPU datapoints found for instance {instance_id}")
    
    # Stop idle instances and notify via SNS
    if idle_instances:
        # Stop the idle instances
        ec2_client.stop_instances(InstanceIds=idle_instances)
        print(f"Stopped instances: {idle_instances}")
        
        # Send notification via SNS
        sns_message = f"Stopped idle EC2 instances: {', '.join(idle_instances)}"
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=sns_message,
            Subject="Idle EC2 Instances Stopped"
        )
        
        print("SNS notification sent.")
    else:
        print("No idle instances found.")
