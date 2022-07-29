import os
import pickle
import boto3
import pandas as pd
from random import randint

PREFIX = 'LANDSCAPE_APP_'

# If running locally, read data from the filesystem
if 'sferg' in os.path.expanduser('~'):
  PATH = 'data/'
  df = pd.read_csv(PATH + PREFIX + 'Proposal_Similarity_DataFrame.csv')
  embeddings = pickle.load(open(PATH + PREFIX + 'embeddings.pkl', 'rb'))
  knn_indices = pickle.load(open(PATH + PREFIX + 'knn_indices.pkl', 'rb'))
  topics = pickle.load(open(PATH + PREFIX + 'topics.pkl', 'rb'))

# Otherwise read data from S3
else:
  BUCKET = 'lfc-landscape'
  s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['AWS_ACCESS_SECRET']
    )
  
  df = pd.read_csv(
    s3.get_object(
      Bucket=BUCKET,
      Key=PREFIX + 'Proposal_Similarity_DataFrame.csv'
      )['Body']
    )
  embeddings = pickle.loads(
    s3.get_object(
      Bucket=BUCKET,
      Key=PREFIX + 'embeddings.pkl'
      )['Body'].read()
    )
  knn_indices = pickle.loads(
    s3.get_object(
      Bucket=BUCKET,
      Key=PREFIX + 'knn_indices.pkl'
      )['Body'].read()
    )
  topics = pickle.loads(
    s3.get_object(
      Bucket=BUCKET,
      Key=PREFIX +'topics.pkl'
      )['Body'].read()
  )

# Assign the x, y, z coordinates here so we don't do this every time the graph is re-generated
df['nodes_x'] = [x[0] for x in embeddings]
df['nodes_y'] = [x[1] for x in embeddings]
df['nodes_z'] = [x[2] for x in embeddings]

COMPETITION_COLORS = {
  '100Change2020': '#0028f2',
  'Climate2030': '#1aff00',
  'ChicagoPrize': '#ffae00',
  'ECW2020': '#33752d',
  'EO2020': '#f20081',
  'LLIIA2020': '#ffff00',
  'LoneStar2020': '#666565',
  'RacialEquity2030': '#ff0000',
  'Democracy22': '#00e6f2',
  'BaWoP22': '#a88532'
  }

COMPETITION_NAMES = {
  '100Change2020': '100&Change2020',
  'Climate2030': '2030ClimateChallenge',
  'ChicagoPrize': 'Chicago Prize',
  'ECW2020': "Equality Can't Wait",
  'EO2020': 'Economic Opportunity Challenge',
  'LLIIA2020': 'LLIA',
  'LoneStar2020': 'Lone Star Prize 2020',
  'RacialEquity2030': 'Racial Equity 2030',
  'Democracy22': 'Stronger Democracy Award',
  'BaWoP22': 'Build a World of Play',
  }

TOPIC_COLORS = [
  '#%06X' % randint(0x444444, 0xFFFFFF) for i in range(len(topics.keys()) - 1)
  ]
