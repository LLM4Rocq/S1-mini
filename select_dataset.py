import json
import re
import os

# Define possible selecting techniques

selectors = {
    "100_900": lambda l: l[:100] + l[-900:],
    "mid_1000": lambda l: l[len(l)//2-500:len(l)//2+500],
    "q9_1000": lambda l: l[9*len(l)//10-500:9*len(l)//10+500],
    "inf_1000": lambda l: l[:1000]
}


def format_theorem(thm):
    """Retrieve the statement and the proof of a theorem."""
    match = re.match(r"(?P<statement>(Lemma|Theorem)[\s\S]*)(?P<proof>Proof.[\s\S]*(Defined|Qed).)", thm)

    if match is None:
        print(thm[:50])
        exit(1)
    else:
        statement = match.group("statement")
        proof = match.group("proof")
        return {"statement": statement, "proof": proof}

def make(selector, data_info):
    """Select theorems with the `selector`, format them and save them."""

    savefile = f"data/selected/{data_info}_{selector}.jsonl"

    if os.path.exists(savefile):
        print("Selected dataset already here.")
    else:

        print("Making the selected dataset:")

        print("  Download the data ...")
        datafile = f"data/scored/{data_info}.json"
        with open(datafile, "r") as file:
            data = json.load(file)
            scores_thms = list(zip(data["scores"], data["theorems"]))

        print("  Rank the theorems ...")
        scores_thms.sort()
        theorems = [thm for _, thm in scores_thms]

        print("  Format the theorems ...")
        theorems = list(map(format_theorem, theorems))

        print("  Select theorems ...")
        select_function = selectors[selector]
        selected_theorems = select_function(theorems)

        print("  Saving the selected data ...")
        with open(savefile, "w") as file:
            for thm in selected_theorems:
                thm = json.dumps(thm, indent=2)
                file.write(thm + "\n")

        print("  DONE!")

    return f"{data_info}_{selector}"
