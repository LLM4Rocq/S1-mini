import re

from chain_of_thought import Prompter

system_prompt = """# Coq Code Commenting Task

## Context

You are a researcher specializing in formal verification, the Coq proof assistant, and machine learning.
As part of your work, you aim to fine-tune large language models (LLMs) to write Coq proofs. For this, you need a high-quality dataset of Coq theorems and their corresponding informal explanations.

Following the methodology from a reference paper, you plan to fine-tune your models using a curated dataset of 1000 theorems of exceptionally high quality.

Each entry in this dataset should contain three components:
- The Coq theorem: its statement and proof, written in Coq.
- An exhaustive informal proof: a detailed and precise explanation of the proof in natural language, fully aligned with the Coq version.
- A structured mapping: a step-by-step explanation showing how the informal proof was translated into Coq code.

Currently, only the first component (Coq statement and proof) is available.
Your task is to generate the remaining two components, one theorem at a time.

## Input

For each task, you will receive:
- this instruction prompt;
- the statement of a theorem in Coq;
- Its corresponding proof written using ssreflect, the tactic language used in the mathcomp library (note: ssreflect differs from standard Coq tactics).

## What You Should Do

For each given theorem:
- Write an exhaustive informal version of the proof: cover every step and reasoning detail, matching the structure and content of the Coq proof.
- Write a structured explanation of how the informal proof was translated into Coq: align each informal reasoning step with the corresponding Coq tactics.

## Formatting Guidelines

To ensure consistency, use the following tags in your output:
- Write the informal proof in a ### Proof section.
- Write the informal-to-Coq mapping in a ### Mapping section.
"""

user_prompt = """## Theorem Task

You are now given the following Coq theorem and its proof:

```coq
{statement}
{proof}
```

Write the informal proof and the informal-to-Coq mapping using the guidelines above.
"""

def parse(resp: str) -> tuple[str, str]:
    print("RESP:\n", resp)
    proof = re.search(r"###\s*(Proof|proof)\s*([\s\S]*?)\s*###", resp)
    proof = proof.group(1)

    mapping = re.search(r"###\s*(Mapping|mapping)\s*([\s\S]*)(###|\s*)", resp)
    mapping = mapping.group(1)

    return proof, mapping

def format(thm: dict[str, str], result: tuple[str, str]) -> dict[str, str]:
    proof, mapping = result
    return {
        "rocq_statement": thm["statement"],
        "rocq_proof": thm["proof"],
        "informal_proof": proof,
        "mapping": mapping
    }

prompter = Prompter(system_prompt, user_prompt, parse, format)
