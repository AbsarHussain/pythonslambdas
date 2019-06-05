from email.header import Header
import boto3 
import datetime
from datetime import date, timedelta
from boto3.dynamodb.conditions import Key
sqs = boto3.resource('sqs') 
dynamodb = boto3.resource('dynamodb')
def lambda_handler(event, context):
    sum=0
    count=0
    today_date = date.today()
    str_today_date=today_date.strftime("%m%d%y")
    today_day=str_today_date[2:4]
    print (today_day)
    # print("First one")
    queue = sqs.get_queue_by_name(QueueName='queuee_name')
    print(queue.url)
    print(queue.attributes.get('ApproximateNumberOfMessages'))
    messages_count=queue.attributes.get('ApproximateNumberOfMessages')
    
    table = dynamodb.Table('Table_name')
    # print("check3")
    # table = dynamodb.Table('Movies')
    if today_day>5:
        ondb_data,twdb_data,thdb_data,fodb_data,fidb_data=None,None,None,None,None
        ondb_date =str(date.today()- timedelta(days=1))
        twdb_date =str(date.today()- timedelta(days=2))
        thdb_date =str(date.today()- timedelta(days=3))
        fodb_date =str(date.today()- timedelta(days=4))
        fidb_date =str(date.today()- timedelta(days=5))
        print(ondb_date,twdb_date,thdb_date,fodb_date,fidb_date)
		#this dynamo db query is used, I have fetched five values one by one but using the list it can be looped
        response = table.query(
        KeyConditionExpression=Key('date').eq(ondb_date)
        )
        for i in response['Items']:
            ondb_data=i['messages_count']
            print("thisone")
            print(ondb_date)
            print(ondb_data)
            
        response = table.query(
        KeyConditionExpression=Key('date').eq(twdb_date)
        )
        for i in response['Items']:
            twdb_data=i['messages_count']
            print("secondone")
            print(twdb_date)
            print(twdb_data)
            
        response = table.query(
        KeyConditionExpression=Key('date').eq(thdb_date)
        )
        for i in response['Items']:
            thdb_data=i['messages_count']
            print("secondone")
            print(thdb_date)
            print(thdb_data)
            
        response = table.query(
        KeyConditionExpression=Key('date').eq(fodb_date)
        )
        for i in response['Items']:
            fodb_data=i['messages_count']
            print("secondone")
            print(fodb_date)
            print(fodb_data)
            
        response = table.query(
        KeyConditionExpression=Key('date').eq(fidb_date)
        )
        for i in response['Items']:
            fidb_data=i['messages_count']
            print("secondone")
            print(fidb_date)
            print(fidb_data)
        #loop will end here
		#if else case this can also be converted into a list to reduce the number of lines and follow a better procedure
        if ondb_data is None:
                count=count
                print (count)
                
        else:
                count=count+1
                print (count)
                sum=int(ondb_data)
        if twdb_data is None:
                count=count
                print (count)
                
        else:
                count=count+1
                print (count)
                sum=sum+int(twdb_data)
        if thdb_data is None:
                count=count
                print (count)
                
        else:
                count=count+1
                print (count)
                sum=sum+int(thdb_data)
        if fodb_data is None:
                count=count
                print (count)
                
        else:
                count=count+1
                print (count)
                sum=sum+int(fodb_data)
        if fidb_data is None:
                count=count
                print (count)
                
        else:
                count=count+1
                print (count)
                sum=sum + int(fidb_data)
		#loop ends here
		
        print("average is ", sum/count)
    response = table.query(
    KeyConditionExpression=Key('date').eq('2019-05-31')
    
    )
    for i in response['Items']:
        print(i['messages_count'], ":", i['messages_count'])
    today_date = date.today()- timedelta(days=1)
    print (today_date.strftime("%m%d%y"))
    today_date = str(date.today()- timedelta(days=6))
    average=sum/count
    if average >  messages_count:
        status= 'true'
        response = table.put_item(
            Item={
            'date': today_date,    
            'messages_count':messages_count,
            'status': status
        }
        )
    if average <  messages_count:
        status= 'true'
        response = table.put_item(
            Item={
            'date': today_date,    
            'abnormal_messages_count':messages_count,
            'status': status
        }
        )
    if average <  messages_count:
        msg = MIMEMultipart()
        msg['From'] = 'Email Sender email'
        msg['To'] = 'Email To'
        msg['Subject'] = 'Lambda Alarm'
        text = 'Lambda Function'
        html_str = """\
        <html>
          <head></head>
          <body>
            <p> """+text+ """<br>
            </p>
          </body>
        </html>
        """    
        body_html = MIMEText(html_str, "html")
        msg.attach((body_html))
        send_to = ['email_to']
        print 'sending mail'
        smtp = smtplib.SMTP('insig-Outgo-FDPNUQ0UKAC4-8c4e06621634b50d.elb.us-east-1.amazonaws.com')
        smtp.sendmail('Email_from', send_to, msg.as_string())
        return {
            'statusCode': 200,
            'body': json.dumps('Lambda Succesful')
        }
