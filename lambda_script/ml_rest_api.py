import flask
import csv
import json
import boto3
import pickle
import pandas as pd
from flask import request
from helper import process_text
from tensorflow.keras.preprocessing import sequence

ENDPOINT_NAME='tinggitecc-fnd-model-endpoint'

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['POST'])
def handler():
    print(request.get_json())
    article = request.get_json()['data']['article']
    cleanedArticleNoStem = process_text(article, length=False, stem=True)
    df = pd.DataFrame([cleanedArticleNoStem], columns=['article'])

    with open('tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)

    seq = tokenizer.texts_to_sequences(df['article'])
    seq = sequence.pad_sequences(seq, maxlen=500, padding='post')
    seq = pd.DataFrame(seq)

    payload = seq.to_csv(header=False, index=False)

    # Call sagemaker endpoint
    session = boto3.Session(profile_name='s3-bucket')
    runtime = session.client('runtime.sagemaker')
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                           ContentType='text/csv',
                                           Body=payload)

    result = json.loads(response['Body'].read().decode())
    print(result)

    return result

app.run()
