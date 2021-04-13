import boto3
from botocore.config import Config
import traceback
import json
import datetime


AWS_PROFILE_NAME = '__REPLACE_ME__'

REGIONS = (
    'us-east-1',
    'us-east-2',
    'us-west-1',
    'us-west-2',
    'af-south-1',
    'ap-east-1',
    'ap-south-1',
    'ap-northeast-3',
    'ap-northeast-2',
    'ap-northeast-1',
    'ap-southeast-1',
    'ap-southeast-2',
    'ca-central-1',
    'eu-central-1',
    'eu-west-1',
    'eu-west-2',
    'eu-west-3',
    'eu-south-1',
    'eu-north-1',
    'me-south-1',
    'sa-east-1',
)

ARCHITECTURES = (
    'x86_64',
    'arm64',
)


def get_latest_ami_image_id(data: list, architecture: str='x86_64')->str:
    latest_timestamp = 0
    image_id = None
    for image_details in data:
        if image_details['Architecture'] == architecture:
            if image_details['Timestamp'] > latest_timestamp:
                latest_timestamp = image_details['Timestamp']
                image_id = image_details['ImageId']
    return image_id


aws_data_set_processed = dict()
aws_data_set_processed['Regions'] = dict()
for region in REGIONS:
    print('Retrieving data for region "{}"'.format(region))
    aws_data_set_processed['Regions'][region] = list()
    session = boto3.Session(profile_name=AWS_PROFILE_NAME)
    request_config = Config(region_name=region)
    client = session.client('ec2', config=request_config)   
    response = None
    try:
        response = client.describe_images(
            Filters=[
                { 'Name': 'architecture', 'Values': ['x86_64', 'arm64',] },
                { 'Name': 'image-type', 'Values': ['machine',] },
                { 'Name': 'is-public', 'Values': ['true',] },
                { 'Name': 'owner-alias', 'Values': ['amazon',] },
                { 'Name': 'state', 'Values': ['available',] },
                { 'Name': 'virtualization-type', 'Values': ['hvm',] },
                { 'Name': 'hypervisor', 'Values': ['xen',] },
                { 'Name': 'root-device-type', 'Values': ['ebs',] },
            ]
        )
    except:
        print('\tFAILED to retrieve data for region')
    if response is not None:
        if 'Images' in response:
            print('\tRetrieved {} records'.format(len(response['Images'])))
            for image in response['Images']:
                if 'Description' in image:
                    if 'Amazon Linux 2' in image['Description'] and 'HVM gp2' in image['Description']:
                        extracted_data = dict()
                        extracted_data['Architecture'] = image['Architecture']
                        extracted_data['CreationDate'] = image['CreationDate']
                        extracted_data['ImageId'] = image['ImageId']
                        date_time_obj = datetime.datetime.strptime(image['CreationDate'], '%Y-%m-%dT%H:%M:%S.%f%z')
                        extracted_data['Timestamp'] = int(date_time_obj.timestamp())
                        aws_data_set_processed['Regions'][region].append(extracted_data)


print('FINAL PROCESSING')
final_result = dict()
for region in REGIONS:
    print('Processing region "{}"'.format(region))
    final_result[region] = dict()
    for architecture in ARCHITECTURES:
        latest_ami_image_id = get_latest_ami_image_id(data=aws_data_set_processed['Regions'][region], architecture=architecture)
        if latest_ami_image_id is not None:
            final_result[region][architecture] = latest_ami_image_id


print('Writing Data to file')
with open('ec2_ami_images.json', 'w') as f:
    f.write('{}'.format(json.dumps(final_result)))


print('DONE')
print()
    

