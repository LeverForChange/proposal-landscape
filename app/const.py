import os
import pickle
import boto3
import pandas as pd
from random import randint

# If running locally, read data from the filesystem
if 'sferg' in os.path.expanduser('~'):
  PATH = 'data/'
  df = pd.read_csv(PATH + 'lfc-proposals-clean.csv')
  embeddings = pickle.load(open(PATH + 'embeddings.pkl', 'rb'))
  knn_indices = pickle.load(open(PATH + 'knn_indices.pkl', 'rb'))
  topics = pickle.load(open(PATH + 'topics.pkl', 'rb'))

# Otherwise read data from S3
else:
  BUCKET = 'lfc-landscape'
  s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['AWS_ACCESS_SECRET']
    )
  
  df = pd.read_csv(
    s3.get_object(Bucket=BUCKET, Key='lfc-proposals-clean.csv')['Body']
    )
  embeddings = pickle.loads(
    s3.get_object(Bucket=BUCKET, Key='embeddings.pkl')['Body'].read()
    )
  knn_indices = pickle.loads(
    s3.get_object(Bucket=BUCKET, Key='knn_indices.pkl')['Body'].read()
    )
  topics = pickle.loads(
    s3.get_object(Bucket=BUCKET, Key='topics.pkl')['Body'].read()
  )

# Assign the x, y, z coordinates here so we don't do this every time the graph is re-generated
df['nodes_x'] = [x[0] for x in embeddings]
df['nodes_y'] = [x[1] for x in embeddings]
df['nodes_z'] = [x[2] for x in embeddings]

COMPETITION_COLORS = {
  '100andchange': '#0028f2',
  '2030ClimateChallenge': '#1aff00',
  'chicagoprize': '#ffae00',
  'ECWC2020': '#33752d',
  'eoc2019': '#f20081',
  'LLIIA2020': '#ffff00',
  'LSP2020': '#666565',
  'RE2020': '#ff0000',
  'SDA2021': '#00e6f2',
  'BaWoP22': '#a88532'
  }

COMPETITION_NAMES = {
  '100andchange': '100&Change',
  '2030ClimateChallenge': '2030ClimateChallenge',
  'chicagoprize': 'Chicago Prize',
  'ECWC2020': "Equality Can't Wait",
  'eoc2019': 'Economic Opportunity Challenge',
  'LLIIA2020': 'LLIA',
  'LSP2020': 'Lone Star Prize',
  'RE2020': 'Racial Equity',
  'SDA2021': 'Stronger Democracy Award',
  'BaWoP22': 'Build a World of Play',
  }

TOPIC_COLORS = ['#%06X' % randint(0x444444, 0xFFFFFF) for i in range(len(topics.keys()) - 1)]