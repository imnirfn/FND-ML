import os
import io
import csv
import json
import boto3
import pickle
import pandas as pd
from tensorflow.keras.preprocessing import sequence

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    data = json.loads(json.dumps(event))
    article = data['data']
    
    cleanedArticleNoStem = process_text(article, length=False, stem=True)
    df = pd.DataFrame([cleanedArticleNoStem], columns=['article'])

    with open('tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)

    seq = tokenizer.texts_to_sequences(df['article'])
    seq = sequence.pad_sequences(seq, maxlen=500, padding='post')
    seq = pd.DataFrame(seq)

    payload = seq.to_csv(header=False, index=False)

    # Call sagemaker endpoint
    from botocore.config import Config

    session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    runtime = session.client('runtime.sagemaker')
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                           ContentType='text/csv',
                                           Body=payload)

    result = json.loads(response['Body'].read().decode())
    print(result)
    
    return predicted_label
