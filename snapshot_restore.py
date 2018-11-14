###################################################################
#Script Name: AWS Snapshot restore                                                                                             
#Description: The script asks for a snapshot id an recreate an
#             instance using the same paramenters associated with 
#             the old instance
#Author       :Luca Licheri
###################################################################

import boto3

snapshot_id = input("Enter the snapshot ID: ")

ec2 = boto3.resource('ec2', region_name="eu-central-1")

snapshot = ec2.Snapshot(snapshot_id) 

#defining variables from old volumes and instances to be used with new isntance
old_volume_id = snapshot.volume_id
old_volume = ec2.Volume(old_volume_id)
old_volume_size = old_volume.size
old_volume_type = old_volume.volume_type
old_instance_id = old_volume.attachments[0]['InstanceId']
old_instance = ec2.Instance(old_instance_id)
old_instance_type = old_instance.instance_type
key_pair_name = old_instance.key_pair.name
security_group = []
for iterator in old_instance.security_groups:
    security_group.append(iterator['GroupName'])


image = ec2.register_image(
        Name='ami restored',
        RootDeviceName='xvda',
        VirtualizationType='hvm',
        BlockDeviceMappings=[
            {
                'DeviceName': 'xvda',
                'Ebs': {
                    'SnapshotId': snapshot_id,
                    },
                },
            ],
        )

print('Creating Image...')

image.wait_until_exists(
        Filters=[{
            'Name':'state',
            'Values':['available'],
            }],
    )

image_id = image.image_id

instance = ec2.create_instances(
        BlockDeviceMappings=[{
            'DeviceName':'xvda',
            'Ebs': {
                'VolumeSize': old_volume_size,
                'VolumeType': old_volume_type,
                },
            }],
        InstanceType=old_instance_type,
        MinCount=1,
        MaxCount=1,
        SecurityGroups=security_group,
        ImageId=image_id,
        KeyName=key_pair_name,
        TagSpecifications=[
            {
                'ResourceType': 'instance', 
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'New Instance automatically create'
                        },
                    ]
                },
            ],
        )

print("Creating Instance...")
instance = ec2.Instance(instance[0].id)
instance.wait_until_running()

print("Deregistering Image...")
ami = ec2.Image(image_id)
ami.deregister()

print("The new instance has been created")
