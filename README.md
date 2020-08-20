# TinggiTecc Fake News Detector Machine Learning Prototype

## Approach 1 - Deep Learning Model
----
> Given an article, an algorithm is able to determine whether the article is true or fake (within
> possibility). The problem can be seen as a binary classification problem where the task is to
> preditc a class label (0 for True news, 1 for Fake news) given the title and text of the article.

    
- **Dataset**:
	- Kaggle dataset "Fake and real news Dataset" 
		- https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset
		- List of article with the subject of the article and its title categorized as Fake or True.
		  Contains 20826 True and 17903 Fake articles divided into two files (true.csv & fake.csv)
    
### Andrea Guidi on ML wth Amazon SageMaker
https://towardsdatascience.com/how-i-built-a-simple-fake-news-detector-on-amazon-sagemaker-808bf4e0c490  
https://github.com/guidiandrea/udacityCapstone-FakeNewsDetector  
   
**Solution in General:**
----
- The data, which comes from different sources (CSVs) will be labelled and **stacked(?)**;
- After being stacked, the text features such as "title" and "article" will be **processed** in
  order to generate a meaningful vocabulary **(no hashtags, URLs, weird punctuation and**
  **stopwords)**
  From here, two roads can be followed, depending on the choice of the algorithm.
- If a **Machine Learning** algorithm is used, then it is necessary to create a **Bag of Words**
  representation of the texts, either by using word counts, one hot encoding of term
  **frequencyinverse document frequency that can be used together with other features**
  (extracted from date, for example) to train the model;
- Instead, if a **Deep Learning model** is chosen, such as a Recurrent Neural Network, one could
  think of using **only directly text sequences padded to same length and mapped with a**
  word_to_integer vocabulary. Then, the neural network can be trained to solve a binary
  classification problem with a **binary cross-entropy loss.**

**Recurrent Neural Networks are Neural Networks which have 'memory'** which is maintained along several
time steps, given the input sequence. **This allows, in contrast with classical feedforward neural**
**networks, to work with dynamic and time-varying inputs**. 
**There exist different types of recurrent layers**:
- the simple recurrent layer, 
- the Gated Recurrent Unit 
- the Long Short Term Memory layers.  \
   
**Recurrent Neural Networks parameters are trained with a particular version of backpropagation,**
**called the backpropagation through time**, where the recurrent layers are unfolded and the parameters
can be updated separately for each time step and then averaged (weights are shared between time
steps of the same layer).  
  
**The second model I chose was a Neural Network with a Bidirectional LSTM layer and a single sigmoid**
**output**, to present the binary classification task. The Bidirectionality allows the LSTM to learn not
only what is supposed to come “next”, but also what is the “cause” of what comes next, because in
text sequences the context (so what comes before and after) of a word is really important, thus this
can improve performances.

**Main steps**
----
- **Preprocessing**:
	- I considered **only the article texts** as a feature over which I filtered texts with **length below**
	  **20 and above 500 words to avoid empty sequences or too long sequences**. The texts have already
	  been **filtered by stopwords, weird punctuation and transformed to lowercase**
	- I split the data in **Train, Validation and Test datasets with train_test_split from Sklearn**
	- I applied a **Tokenizer from keras to the Training set** which then I used to transform also
	  **Validation and Test Datasets** (To avoid data leakage) and then padded all sequences to a
	  **max len of 500**
- **The Model**:
	- In the training script (remember that I am on SageMaker) I **define the environment variables**
	  and it is where you **define the model structure**, fit it and **save its artifacts on S3**. This is
	  the structure of the network(training script) I used (Keras).
		- > The training script uses tensorflow.keras Sequential API with a vocabulary size of 80000
		  words (same as the Tokenizer), input length of 500 (max_len of pad_sequences)
		  `Embedding(80000, 128, input_length=500)` and an embedding dimension of 128
		  `(Bidirectional(LSTM(128))`
	- Then you add code to **fit and save the model**; this code will be called by SageMaker during the
	  training job.
	- On the **Instance side, instead, I instantiated a TensorFlow object**, where I set the path to the
	  training script, number and type of instance I want to choose, the IAM role and
	  hyperparameters
		- > Model Building is done with  Tensorflow (ran in the SageMaker compute instance). It
		  takes a training script which uses tensorflow.keras (from an S3 bucket, located in
		  source_train directory in the git repo)
	- With the same strategy, I **deployed my model after training** it
	- And **performed inference on the test set (this can be done both with the predict() API** but also
	  by creating a Batch Transform job in case of larger data):


## Approach 2 - Machine Learning Model
----
> Given multiple documents(article text), an algorithm is able to find the similarity of the articles
> according to their words.

- Solution:
	- Cosine Similarity:
		- Cosine similarity is a metric used to measure how similar the documents are irrespective
		  of their size. Mathematically, it measures the cosine of the angle between two vectors
		  projected in a multi-dimensional space. The cosine similarity is advantageous because even
		  if the two similar documents are far apart by the Euclidean distance (due to the size of
		  the document), chances are they may still be oriented closer together. The smaller the
		  angle, higher the cosine similarity.
		- Also consider soft cosine similarity, that considers words that are in similar categories.
		  Word vectors in this approach is closer to each other if they have similar words such as
		  "hello" and "hey", as oppose to the normal cosine similarity, where they would be farther
		  apart.
