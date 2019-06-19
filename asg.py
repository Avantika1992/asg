from troposphere import Base64,Join,Ref, Template,Parameter
from troposphere.autoscaling import AutoScalingGroup
from troposphere.policies import AutoScalingRollingUpdate
from troposphere.autoscaling import LaunchConfiguration
from troposphere.ec2 import VPC
import troposphere.ec2 as ec2
t = Template()
AvailabilityZone = t.add_parameter(Parameter(
    "AvailabilityZone",
    Default="us-east-1a",
    Type="String",
))
ImageId = t.add_parameter(Parameter(
    "ImageId",
    Type="String",
))
LaunchConfiguration = t.add_resource(LaunchConfiguration(
    "LaunchConfiguration",
    ImageId="ami-004a75cc959a0a895",
    InstanceType="t2.micro",
    UserData=Base64(Join('', [
        "#!/bin/bash -xe\n",
        "yum install -y aws-cfn-bootstrap\n",
        "/opt/aws/bin/cfn-signal -e 0 --stack ", { "Ref": "AWS::StackName" },
        " --resource AutoScalingGroup ",
        " --region ", { "Ref" : "AWS::Region" }, "\n"
    ])),
))
AutoScalingGroup = t.add_resource(AutoScalingGroup(
    "AutoScalingGroup",
    AvailabilityZones=Ref(AvailabilityZone),
    DesiredCapacity=1,
    MaxSize=2,
    MinSize=1,
    UpdatePolicy=AutoScalingRollingUpdate(MinInstancesInService=1),
    LaunchConfigurationName=Ref(LaunchConfiguration)
))

print(t.to_json())
