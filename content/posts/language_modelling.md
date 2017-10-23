title: Intro to NLP and Language Modelling
date: 22-10-2017

# An introduction to Language Modelling

## Generative language models
An ongoing problem in Machine Learning is: how do I generate data that _looks like_ some given dataset? For example, it might be useful to know which notes finish a bar of music to make it sound like Jazz. In designing a text-to-speech algorithm, one would need to generate a sequence of sounds which best match the text. It may be useful to generate images just by feeding a caption into an algorithm.  It might also be useful to make the responses of a chatbot _feel natural_ given the entire history of its conversation with the user. Even in machine translation, you would like to **generate** a sequence in Language $T$ given the same sequence but in language $S$. Deep learning has provided a huge boost to all of these fields in recent years.

**Problem: what is the probability of word y given the preceding sequence $\{x_i\}$?**
## Learning conditional probabilities
One way of learning the conditional probability distributions is by getting a large corpus of text and counting up all of the times word _x comes before word _y_ for all _x_ and _y_. This would mean that you would have the likelihood that _y_ should come after _x_ and allow you to model language. Rather than just looking the single previous word, we could enhance the model by looking at both _x_t-1_ and _x_t-2_, known as a **bigram**, for example in:

** She itched her elbow **

there are 3 bigrams - "She itched", "itched her", "her elbow". If the sequence so far is "She itched", then it wouldn't be so obvious that the next word in the sequence should be "her" if you are only given the previous word "itched". However, by being given the bigram "She itched", the probabilty that the next word is "her" is likely to change. Whether or not the probability of getting the correct answer increases depends on whether or not the sequence "she itched **her**" is represented in the training data.

Rather than greedily predicting one word at a time to generate complete sequences, it may be better to use a beam search, whereby the next word is chosen because it maximises the probability over the combination of the next few words.

The problem with using Ngram language models is that they cannot make accurate predictions on previous sequences if they have never seen the particular N-grams before. Also, going to higher orders of N means that the size of the probability distributions increase enormously. Rather than just having the probabilities of each word given each preceding word, a `(vocab_size, vocab_size)` matrix. Cannot remember long term dependencies unless it has seen exactly this scenario before, for example how would it know to close a quotation mark of a quote it had never seen before?


- Par 1: Problem statement and uses for language models

- par 2: Language modelling to 1st order = learning conditional probability distributions
    - Discuss N-Gram models
    - Using Ngram conditional Probability distributions. Greedy vs. beam search.
    - Failings of Ngram method. Lack of distributed representations, no sense of
    closeness unless exact examples have been seen before.

- par 3: LSTMs
    - RNNs and learning long-distance dependencies. LSTMs.
    - Vocabulary size contraints for Ngram vs. LSTM
    - LSTM language model code. Making predictions - greedy vs. beam search.

- par 4: Going deeper
    - Multiple layers and the effects on fluency.
