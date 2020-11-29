
from simple_elmo import ElmoModel
import numpy as np
import time

if __name__ == "__main__":

    # Process only the first k sentences
    max_sentences = 100

    sentences = ["Привет, мир!", "Надо отправить сообщение. В цехе до сих пор не была установлена седьмая центрифуга, а по плану мы должны уже на ней работать"]

    sentences = [s.split()[:100] for s in raw_sentences]

    print("=====")
    print(f"{len(sentences)} sentences total")
    print("=====")

    model = ElmoModel()

    model.load("212")

    # Actually producing ELMo embeddings for our data:
    start = time.time()
    elmo_vectors = model.get_elmo_vectors(sentences, layers="average")
    end = time.time()

    processing_time = int(end - start)

    print(f"ELMo embeddings for your input are ready in {processing_time} seconds")
    print(f"Tensor shape: {elmo_vectors.shape}")

    # Due to batch processing, the above code produces for each sentence
    # the same number of token vectors, equal to the length of the longest sentence
    # (the 2nd dimension of the elmo_vector tensor).
    # If a sentence is shorter, the vectors for non-existent words are filled with zeroes.
    # Let's make a version without these redundant vectors:
    cropped_vectors = []
    for vect, sent in zip(elmo_vectors, sentences):
        cropped_vector = vect[: len(sent), :]
        cropped_vectors.append(cropped_vector)

    # A quick test:
    # in each sentence, we find the tokens most similar to a given token of a given sentence
    query_sentence_nr = -2
    query_word_nr = 1
    query_word = sentences[query_sentence_nr][query_word_nr]
    print(f"Query sentence: {sentences[query_sentence_nr]}")
    print(f"Query: {query_word}")
    query_vec = cropped_vectors[query_sentence_nr][query_word_nr, :]

    print(f"Most similar words (dot product values in parentheses)")

    for sent_nr, sent in enumerate(sentences[:10]):  # we are checking the first 10 sentences
        print("======")
        print(sent)
        sims = {}
        for nr, word in enumerate(sent):
            w_vec = cropped_vectors[sent_nr][nr, :]
            sims[word] = np.dot(query_vec, w_vec)

        for k in sorted(sims, key=sims.get, reverse=True):
            print(k, sims[k])
