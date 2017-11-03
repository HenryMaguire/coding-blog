title: Language Modelling in Python
date: 22-10-2017
next: one_word_story_p1
picture: "http://via.placeholder.com/500x300"
summary: "How to make a bot talk: N-gram models and Recurrent Neural Networks."

# An introduction to Language Modelling
#(_in Python and Tensorflow_)

### Generative language models
An ongoing problem in Machine Learning is: how do I generate data that _looks like_ some given dataset? For example, it might be useful to know which notes finish a bar of music to make it sound like Jazz. In designing a text-to-speech algorithm, one would need to generate a sequence of sounds which best match the text. It may be useful to generate images just by feeding a caption into an algorithm.  It might also be useful to make the responses of a chatbot _feel natural_ given the entire history of its conversation with the user. Even in machine translation, you would like to **generate** a sequence in Language $T$ given the same sequence but in language $$S$$. Deep learning has provided a huge boost to all of these fields in recent years.



**The problem I would like to solve in this article is:**

_How can I build the best possible generative language model given that:_

### _I am not a computational linguist, just an aspiring Machine Learning researcher with decent Python skills_

By this I mean that I do not want to hard code any linguistic rules into my models and I would like to appeal to domain knowledge about the English language as little as possible. This is for a few reasons:

- This makes it generalisable, so if I wanted to apply this model to a different language which operates with totally different rules then I am free to do so by simply swapping out the training data.

- This avoids the steep learning curve of having to go and learn an entire new branch of science. Essentially the AI does this process _for us_ (the whole point, right?).


###_I do not own a GPU, so am reliant on expensive cloud computing resources_

I recently graduated from the [Udacity Machine Learning Engineer Nanodegree](http://www.udacity.com) which requires you to complete a _capstone project_ - essentially a research project of your choosing that you define, propose, implement and write up. My project proposal was to build an end-to-end [Neural Machine Translation]() (NMT) system which outperforms a _dictionary-based_ benchmark. There was a time-limit within which I had to complete this project and - inevitably, due to PhD, life and distractions - I ended up doing much of the work in the weeks leading up to the deadline. Due to this severe shortage of time, I ended up cutting corners - thinking that getting to training the model as quickly as I could would mean that I could finish sooner. However, I missed out many important things that would have helped me along the way and would have saved me around 50% of the coding time and 80% of the compute time I actually ended up using. In the end I had to just throw time, stress and money at my problems to make them go away but here are a few questions that I wish I'd have answered before writing any code:

#### 1) What will the model architecture look like and how will it make predictions?
Let's assume that we've decided on a solution. In the case of the NMT this was [Encoder-Decoder] architecture, where two RNNs are stitched together - one encodes a sequence in the source language into a representation that the second RNN can be conditioned on in order to output the phrase in the target language. I blindly followed a tutorial which didn't properly account for how the inputs would change between training and testing time, which meant that I ended up training a model which I couldn't even test.

#### 2) What does your data actually _look like_?
In the NMT, I had to feed sentences into a model in both French and English. The [dataset I used](http://google.com/WMT14) contained sentences which ranged being from 1 to 125 words long. In reality, the relative likelihood of long sequences was very low (median length was 18 words) but their presence meant that the ends of data batches needed to be padded with many zeros in order to be fed into the RNN. Naively including these long sequences meant that my simple model could not learn anything from the sparse input data and training time was exceptionally long. This simple oversight wasted many hours of GPU and developer time.

#### 3) What are the performance bottlenecks going to be?
From the previous example we have seen that sequence length was a large contributor to training time. Another huge performance cost for Neural Machine Translators is _vocabulary size_. As we will see, when gaining predictions from Deep Learning models we will have to project the RNN hidden layer outputs to a probability space over the words of a vocabulary. The number of parameters in our model is sensitively dependent on the size of this projection layer. Size of projection layer = size of target language vocabulary. However, removing too many words can render the preprocessed data unintelligible so it's a delicate balancing act. This exact reason is why chat bots and translation systems work so much better for closed domain problems, i.e. talking about subjects with specific topics (such as law or business) and so have far smaller vocabularies than for general conversation.

So naturally the last question is...
#### 4) How are you going to pre-process the data to meet these performance requirements?




So essentially what I learned is: **BE RIGOROUS** and **make sure you know exactly what you are about to train**. This might sound obvious or self-evident, but I'm used to cowboy science.


**Why should we solve this problem?**

Well... for fun! Once you have trained this type of model on some dataset it becomes possible to generate new data which _looks like_ the old data. This has been shown numerous times across the web, notably in [Andrej Karpathy's blog](http://www.google.com) where a character level RNN (using LSTMs) was able to generate almost-compilable `C++` code(!) amongst other incredible things. Once you have the conditional probability distributions you need to start generating sequential data, you can also calculate scores for _how likely_ a given sentence. For example, you could use a language model to calculate the probability of the output of a machine translation system, which overall is likely to more expensive to train (more parameters). This scoring system could conversely be used to evaluate how probable a model with a particular architecture or hyperparameters finds a small validation set. A model that finds the validation set more probable is likely to be one that has learned more of the word dependencies and linguistic structure. This type of validation scoring is not something I have seen before (please point me to some references in the comments) but I will try it out in this post.

Rather than try to speak generally on the topic of language models or to reinvent the wheel I am going apply the knowledge gained from this study to the creation of a fun story-telling app in [later posts](/one_word_story_p1). This will require the model to make predictions in real-time, so we will need keep track of the performance of the algorithms at prediction time as well as during training, for each architecture I try.

## The Data
In keeping with the story-telling theme, I have scraped all of the fiction from [this](http://textfiles.com/fiction) open source collection of text files. These stories vary in wildly in theme and length and total 2.3 million tokens. At only around 13MB this is probably not enough data to train a deep learning model on but it will do for development purposes.

**Problem: what is the probability of word y given the preceding sequence $\{x_i\}$?**
## Learning conditional probabilities
One way of learning the conditional probability distributions is by getting a large corpus of text and counting up all of the times word _x comes before word _y_ for all _x_ and _y_. This would mean that you would have the likelihood that _y_ should come after _x_ and allow you to model language. Rather than just looking the single previous word, we could enhance the model by looking at both _x_t-1_ and _x_t-2_, known as a **bigram**, for example in:

** She itched her elbow **

there are 3 bigrams - "She itched", "itched her", "her elbow". If the sequence so far is "She itched", then it wouldn't be so obvious that the next word in the sequence should be "her" if you are only given the previous word "itched". However, by being given the bigram "She itched", the probabilty that the next word is "her" is likely to change. Whether or not the probability of getting the correct answer increases depends on whether or not the sequence "she itched **her**" is represented in the training data.

Rather than greedily predicting one word at a time to generate complete sequences, it may be better to use a beam search, whereby the next word is chosen because it maximises the probability over the combination of the next few words.

**Preprocessing the data**

The problem with using Ngram language models is that they cannot make accurate predictions on previous sequences if they have never seen the particular N-grams before. Also, going to higher orders of N means that the size of the probability distributions increase further. Rather than just having the probabilities of each word given each preceding word, a `(vocab_size, vocab_size)` matrix. Cannot remember long term dependencies unless it has seen exactly this scenario before, for example how would it know to close a quotation mark of a quote it had never tried to complete before?



## Long Short-Term Memory

- RNNs and learning long-distance dependencies. LSTMs.

- Vocabulary size contraints for Ngram vs. LSTM

- LSTM language model code. Making predictions - greedy vs. beam search.

- Comparison of LSTM to GRU

## Going deeper

- Multiple layers and the effects on fluency.


# TODO:

- Look at speed of predictions for each different architecture I try in language_modelling
