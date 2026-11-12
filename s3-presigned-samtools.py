#!/usr/bin/env python3

import argparse
import boto3


client = boto3.client('s3')

parser = argparse.ArgumentParser()
parser.add_argument('s3path')
args = parser.parse_args()

s3path = args.s3path

tokens = s3path.split('/')
bucket = tokens[2]
key = '/'.join(tokens[3:])

url  = client.generate_presigned_url("get_object", Params={"Bucket":bucket, "Key":key, "RequestPayer":'requester'})
print(url)