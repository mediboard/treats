def removekey_oop(d, key):
    r = dict(d)
    del r[key]
    return r


def get_embedding(text, model="text-embedding-ada-002"):
    import openai

    text = text.replace("\n", " ")
    return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']


def calculate_results_summary(mean, mn):
    if (mn and mn <= .15):
        return 10 if mean <= .15 else 8 

    return 0

