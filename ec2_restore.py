###################################################################
#Script Name: AWS EC2 restore 
#Description: The script asks for an Instance id an recreate it
#             using the same paramenters associated with 
#             the old instance
#Author:      Luca Licheri
###################################################################
import boto3

instance_id = input("Enter the instance ID: ")

ec2 = boto3.resource('ec2', region_name="eu-west-2")

instance = ec2.Instance(instance_id)

security_groups = []
for security_group in instance.security_groups:
    security_groups.append(security_group['GroupName'])

for volume in instance.volumes.all():
    volume_size = volume.size
    volume_type = volume.volume_type

image = instance.create_image(
        Name="restore_ami"
        )

print("Creating AMI...")

image.wait_until_exists(
        Filters=[{
            'Name':'state',
            'Values':['available'],
            }],
    )

new_instance = ec2.create_instances(
        BlockDeviceMappings=[{
            'DeviceName':'xvda',
            'Ebs': {
                'VolumeSize': volume_size,
                'VolumeType': volume_type,
                },
            }],
        InstanceType=instance.instance_type,
        MinCount=1,
        MaxCount=1,
        SecurityGroups=security_groups,
        ImageId=image.image_id,
        TagSpecifications=[
            {
                'ResourceType': 'instance', 
                'Tags': instance.tags                },
            ],
        )


print("Creating Instance...")
new_instance = ec2.Instance(new_instance[0].id)
new_instance.wait_until_running()

for volume in instance.volumes.all():
    volume.create_tags(Tags=instance.tags)

ami = ec2.Image(image.image_id)
ami.deregister()

print("The new instance has been created")
