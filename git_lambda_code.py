import math #for additional mathematical funtions
import os
import json
import smtplib
import email #these can be used if you are trying to send email through lambda but will require smtp outgoing ec2
import boto3 
import datetime
from datetime import date, timedelta #for manipulating time
from operator import truediv #for floating point division

def lambda_handler(event, context):
    date_string =date.today
    start_time=datetime.datetime.now()- timedelta(days=6) # gets past five days and todays data, it can fetch data of last 14days
    end_time=datetime.datetime.now()
    seconds_in_one_day = (86400)  # used for granularity ,represents seconds in one day
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
      MetricDataQueries=[
          {
              'Id': 'm1',
              'MetricStat': {
                  'Metric': {
                      'Namespace': 'AWS/SQS',
                      'MetricName': 'ApproximateNumberOfMessagesVisible', # Metric name can be different  other attributes can be checked on AWS lambda CW get metric data page
                      'Dimensions': [
                          {
                              'Name': 'QueueName',
                              'Value': 'YOur SQS queue name',
                          },
                          
                      ]
                  },
                  'Period': 86400,
                  'Stat': 'Sum', #instead of sum you can also use Max and average, other attributes can be checked on AWS lambda CW get metric data page
                  'Unit': 'Count' #instead of count you can also use Bytes and Gigabytes, other attributes can be checked on AWS lambda CW get metric data page
              },
              'ReturnData': True,
          },
      ],
      StartTime=start_time,
      EndTime=end_time,
      )
    metric_data_list=[]
    for data in response['MetricDataResults'][0]['Values']: #dictionary element MEtric data result contains time and values of data sample 
      metric_data_list.append(data) #getting all the data values in the metric data list
    today_data=metric_data_list[0]
    yesterdays_data=metric_data_list[1]
    print(metric_data_list)
    del metric_data_list[0]
    print(metric_data_list)
    metric_data_list.sort()#
    total_data=len(metric_data_list)
    print(total_data)
    print("data used", metric_data_list[1:total_data])
	#ignoring top most values because it can be abnormal and can change our average very much
    sqs_average_data=sum(metric_data_list[1:total_data-1])/len((metric_data_list[1:total_data-1]))
    data_difference=[]
    for length in range(total_data-1):
      difference = metric_data_list[length] - metric_data_list[length+1]
      int_difference= int(difference)
      data_difference.append(int(int_difference))
    print("data difference list",data_difference)
    data_difference_length=len(data_difference)
    # print(data_difference_length)
	#here I am using my own logic to  check the usual difference in the values so that we can get estimate difference that can occur, converting negative difference to positive
    for i in range(data_difference_length):
      if data_difference[i] < 0:
        data_difference[i]=-data_difference[i]
    data_difference.sort()
    print("data difference used",sum(data_difference[0:data_difference_length]))
    print("length is ",len(data_difference[0:data_difference_length]))
    diff_added=sum(data_difference[0:data_difference_length])
    diff_length=len(data_difference[0:data_difference_length])
	# in python 2.X truediv is used to return floating values from division, ceil used to prevent decimal values
    average_difference=math.ceil(truediv(diff_added, diff_length))
    print(average_difference)
    print("average_difference is ", average_difference)
    today_data_difference=abs(today_data-yesterdays_data)
    sqs_expected_data=math.ceil(sqs_average_data)+math.ceil(average_difference)
    print(metric_data_list)
    print("todays data difference \n",today_data_difference," todays data \n",today_data," yesterdays data \n",yesterdays_data," sqs average  data \n",sqs_average_data," sqs exp data \n",sqs_expected_data," avg data diff \n",average_difference)
    if today_data>(sqs_average_data+average_difference):
      print("generating SNS") # Email will be sent to all the subscribers of that topic
      sns = boto3.client('sns')
      sns.publish(
          TopicArn = 'arn:(your TOpic ARN here without bracket)',
          Subject = 'SQS Queue Count is abnormal ' ,
          Message = 'SQS Queue Count is abnormal. \n  Todays Number of Messages is : ' + str(today_data) + '\r\n SQS Average Number of Messages is : ' + str(sqs_average_data) + '\r\n And Expected Number of Messages is : ' + str(sqs_expected_data) 
     
    )
asdaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb

	    testing tag fix adasdasssssdasads
