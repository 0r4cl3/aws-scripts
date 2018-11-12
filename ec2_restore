import boto3

ec2 = boto3.resource('ec2', region_name="eu-central-1")

instance = ec2.Instance('i-0473e3ad4cbec0e43')


instance_type = instance.instance_type
security_group = instance.security_groups.first
print(security_group)


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
        )

print("Creating Instance")

new_instance.wait_until_running()
print("done")
