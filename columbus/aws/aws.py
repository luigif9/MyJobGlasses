import boto3
import os
from config import columbus

recommendation_bucket = 'myjobglasses-recommendation'
s3client = boto3.client('s3')

def s3_bucket_upload(local_file, remote_file):
  """upload a file from local to  MJG recommendation bucket"""
  s3client.upload_file(local_file, recommendation_bucket, remote_file)

def s3_bucket_download(remote_file, local_file):
  """download a file from MJG recommendation bucket to local"""
  s3client.download_file(recommendation_bucket, remote_file, local_file)

def pull_file(file_name, local_file=None):
  """Pull a file from Amazon recommendation bucket / ready
  If a second argument is given, override the local file_name
  """
  print('Fetching file "' + file_name + '" from AWS...')

  if local_file:
    data_local_file = os.path.join(columbus.data, local_file)
  else:
    data_local_file = os.path.join(columbus.data, file_name)

  ready_remote_file = config.current_config['RAILS_ENV'] + 'ready/' + file_name
  try:
    s3_bucket_download(ready_remote_file, data_local_file)
    print('File downloaded to ' + data_local_file)
    return data_local_file
  except:
    print('Could not download file : {}'.format(ready_remote_file))
    raise



def push_recommendation_file(local_file, filename):
  """TODO : only the push_file part should be here !
  The caller should specify the name of the file to upload
  """
  patht_archive = columbus.current_config['RAILS_ENV'] + '/processed/archives/columbus/'+ filename 

  patht = columbus.current_config['RAILS_ENV'] + '/processed/columbus-recommendations.json'

  print('Preparing to push file "' + filename + '"to AWS...')
  try:
      s3_bucket_upload(local_file, patht_archive)
      s3_bucket_upload(local_file, patht)
      print('File uploaded!')
  except:
      print('No such file or directory : {}'.format(local_file))
      raise
