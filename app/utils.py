import hashlib


def removekey_oop(d, key):
    r = dict(d)
    del r[key]
    return r


def create_function(name, args, body):
    # Build the function definition string
    func_def = "def {}({}):\n{}\n".format(name, args, body)

    # Create a new namespace to hold the function
    ns = {}

    # Execute the function definition in the new namespace
    exec(func_def, ns)

    # Extract the newly created function from the namespace
    return ns[name]


def count_items(lst):
    """
    Counts the occurrence of each item in a list and returns it as a dictionary.
    """
    count_dict = {}
    for item in lst:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    return count_dict



def get_embedding(text, model="text-embedding-ada-002"):
    import openai

    text = text.replace("\n", " ")
    return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']


def calculate_results_summary(mean, mn):
    if (mn and mn <= .15):
        return 10 if mean <= .15 else 8 

    return 0


def hash_string(string):
    sha256 = hashlib.sha256()
    sha256.update(string.encode())
    return sha256.hexdigest()


def enum2String(enum):
    word = str(enum).split('.')[-1]
    words = word.split('_')
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)