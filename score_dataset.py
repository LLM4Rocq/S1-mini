import os
import re
import bm25s
from tqdm import tqdm
import json

# Define possible similarity scoring techniques

def bm25_get_scores(dataset):
    """Compute bm25 scores of a dataset."""
    stemmer = lambda l: [word for word in l]
    tokenized_dataset = []

    print("Tokenize dataset ...")
    for i, data in enumerate(dataset):
        tokenized_dataset.append(bm25s.tokenize(data, return_ids=False, stemmer=stemmer, show_progress=False)[0])

    bm25 = bm25s.BM25()

    def get_score(data, dataset):
        bm25.index(dataset, show_progress=False)
        scores = bm25.get_scores(data)
        score = sum(scores)

        return score

    scores = []
    print("Compute bm25 scores ...")
    for i, thm in tqdm(list(enumerate(tokenized_dataset))):
        score = get_score(thm, tokenized_dataset[:i] + tokenized_dataset[i+1:])
        scores.append(float(score))

    return scores

scorers = {
    "bm25": bm25_get_scores
}

def get_rocq_files(directory):
    """Retrieve all Rocq files in a directory."""
    files = []
    for path in os.listdir(directory):
        new_path = os.path.join(directory, path)
        if os.path.isfile(new_path):
            if os.path.splitext(path)[1] == ".v":
                files.append(new_path)
        elif os.path.isdir(new_path):
            files += get_rocq_files(new_path)

    return files

def remove_comment_in_file(path):
    """Remove Rocq comments in a file."""
    with open(path, "r") as file:
        content = file.read()

    pattern = re.compile(r"(\(\*[\s\S]*?\*\))")
    comments = pattern.finditer(content)

    for comment in comments:
        content = content.replace(comment.group(1), "")

    name, extension = path.rsplit(".", 1)
    new_path = name + "_uncommented." + extension
    with open(new_path, "w") as file:
        file.write(content)

    return new_path

def get_lemmas_in_file(path):
    """Find all lemmas in a file."""
    with open(path, "r") as file:
        content = file.read()

        pattern = re.compile(r"(?<!\S)(?P<lemma>Lemma\s[\s\S]*?(Defined|Qed).)")
        lemmas = pattern.finditer(content)
        lemmas = [match.group("lemma") for match in lemmas]

    return lemmas

def get_theorems_in_file(path):
    """Find all theorems in a file."""
    with open(path, "r") as file:
        content = file.read()

        pattern = re.compile(r"(?<!\S)(?P<theorem>Theorem\s[\s\S]*?(Defined|Qed).)")
        theorems = pattern.finditer(content)
        theorems = [match.group("theorem") for match in theorems]

    return theorems

def make(dataset, scorer):
    """
    Read all Rocq files in the `directory` and save all theorems.
    Compute the similarity scores of the theorems with the `scorer`.
    Save theorems and scores in a file.
    """

    datafile = f"data/scored/{dataset}_{scorer}.json"

    if os.path.exists(datafile):
        print("Scored dataset already here.")
    else:

        print("Making the scored dataset.")

        print("  Get all Rocq files ...")
        files = get_rocq_files(f"data/raw/{dataset}")

        print("  Remove comments from files ...")
        uncommented_files = list(map(remove_comment_in_file, files))

        print("  Find lemmas in files ...")
        theorems = []
        for lemmas in map(get_lemmas_in_file, uncommented_files):
            theorems += lemmas

        print("  Find theorems in file ...")
        for thms in map(get_theorems_in_file, uncommented_files):
            theorems += thms

        print("  Total number of theorems:", len(theorems))

        for uncommented_file in uncommented_files:
            os.remove(uncommented_file)

        score_function = scorers[scorer]
        scores = score_function(theorems)

        print("  Save the dataset ...")
        with open(datafile, "w") as file:
            json.dump({"theorems": theorems, "scores": scores}, file, indent=2)

        print("  DONE!")

    return f"{dataset}_{scorer}"
