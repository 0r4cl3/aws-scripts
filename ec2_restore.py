import boto3

instance_id = input("Enter the instance ID: ")


ec2 = boto3.resource('ec2', region_name="eu-central-1")

instance = ec2.Instance(instance_id)


instance_type = instance.instance_type
security_group = instance.security_groups[0]['GroupName']

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
        SecurityGroups=[security_group],
        ImageId=image_id,
        )

print("Creating Instance")


ami = ec2.Image(image_id)
ami.deregister

print("done")
