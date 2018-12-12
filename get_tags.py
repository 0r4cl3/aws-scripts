import boto3

ec2 = boto3.resource('ec2', region_name='eu-west-2')

instances = ec2.instances.all()

for instance in instances :
    for tag in instance.tags :
        if tag['Key'] == 'url' :
            with open('ansible.txt', 'a') as file :
                print(tag['Value'] + '.clarionvoip.net', file=file)






