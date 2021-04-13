# aws-ec2-ami-images-per-region

My original goal was to get the latest list of ___Amazon Linux AMI images___ when [creating a mapping in CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html).

At the moment everything is still hard coded - This will eventually get more parameter driven over time. This started as a very quick-and-dirty script to just get the info.

## Getting Started

You will need Python (I'm assuming everyone is using version 3.x by now).

The script depends on [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) to call the AWS API.

At the moment, the script assumes you have configured your [AWS CLI](https://aws.amazon.com/cli/) with [named profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html). You will need an IAM user with API credentials in your profiles that has sufficient privileges for the EC2 [`DescribeImages` API call](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeImages.html). The actual permission you need is `ec2:DescribeImages`.

For now, you will need to edit the Python script and replace the text `__REPLACE_ME__` with the profile name you configured.

## Running the command and the output

An example run is shown below. The resulting JSON output will be in the file `ec2_ami_images.json`. You should be able to just copy and paste this into your CloudFormation template and use parameters to select the region and architecture.

**_Note_**: Depending on your permissions, your output and/or ability to retrieve images from various regions may differ from the examples shown. Also - the script can take some time to run. In my case it took more than 10 minutes to produce the final JSON file.

```shell
$ python3 get_ec2_ami_images.py 
Retrieving data for region "us-east-1"
        Retrieved 8633 records
  .
  .
  .
Retrieving data for region "ap-east-1"
        FAILED to retrieve data for region
Retrieving data for region "ap-south-1"
        Retrieved 6421 records
  .
  .
  .
Retrieving data for region "sa-east-1"
        Retrieved 6611 records
FINAL PROCESSING
Processing region "us-east-1"
Processing region "us-east-2"
  .
  .
  .
Processing region "sa-east-1"
Writing Data to file
DONE
```


