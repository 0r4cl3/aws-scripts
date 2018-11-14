import boto3

instance_id = input("Enter the instance ID: ")


ec2 = boto3.resource('ec2', region_name="eu-central-1")

instance = ec2.Instance(instance_id)


instance_type = instance.instance_type
security_group = []
for iterator in instance.security_groups:
    security_group.append(iterator['GroupName'])

for volume in instance.volumes.all():
    volume_size = volume.size
    volume_type = volume.volume_type

image = instance.create_image(
        Name="restore_ami"
        )
print("Creating AMI")

image.wait_until_exists(
        Filters=[{
            'Name':'state',
            'Values':['available'],
            }],
    )

image_id = image.image_id

new_instance = ec2.create_instances(
        BlockDeviceMappings=[{
            'DeviceName':'xvda',
            'Ebs': {
                'VolumeSize': volume_size,
                'VolumeType': volume_type,
                },
            }],
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        SecurityGroups=security_group,
        ImageId=image_id,
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

print("Creating Instance")
new_instance = ec2.Instance(new_instance[0].id)
new_instance.wait_until_running()

ami = ec2.Image(image_id)
ami.deregister()

print("The new instance has been created")
