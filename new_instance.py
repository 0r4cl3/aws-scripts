###################################################################
#Script Name: AWS Image Creating
#Description: The script creates an new Instance and associate an 
#             ElasticIP
#Author:      Luca Licheri
###################################################################
import boto3

ec2 = boto3.resource('ec2', region_name='eu-west-2')
client = boto3.client('ec2', region_name="eu-west-2")

client_name = input('Enter the client name: ')

instance = ec2.create_instances(
        BlockDeviceMappings=[{
            'DeviceName':'xvda',
            'Ebs': {
                'VolumeSize': 30,
                'VolumeType': 'standard',
                },
            }],
        InstanceType= 't2.small',
        MinCount=1,
        MaxCount=1,
        SecurityGroups= ['3CX v15'],
        ImageId='ami-0c593aade9c7196cc',
        KeyName='ClarionVoIP Key',
        TagSpecifications=[
            {
                'ResourceType': 'instance', 
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': client_name,
                        },
                    ]
                },
            ],
        )


print('Creating Instance...')
instance = ec2.Instance(instance[0].id)
instance.wait_until_running()

print("Insatnce created.")

print('Allocating Elastic IP...')
eip = client.allocate_address(
        Domain='vpc',
        )

print('Associating Elastic IP...')
association = client.associate_address(
        AllocationId = eip['AllocationId'],
        InstanceId = instance.id
        )
print('Assigning Tags...')
client.create_tags(
        Resources=[
            eip['AllocationId'],
            ],
        Tags=[
            {
                'Key': 'Name',
                'Value': client_name,
                },
            ],
        )
print(str(instance.id) + ' ready')
