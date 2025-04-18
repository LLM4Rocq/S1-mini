import score_dataset, select_dataset, chain_of_thought
import proof_prompter, proof_mapping_prompter

def make(directory, scorer, selector, model, vllm_address, prompter):
    scored_dataset = score_dataset.make(scorer, directory)
    selected_dataset = select_dataset.make(selector, scored_dataset)
    return chain_of_thought.make(model, vllm_address, prompter, selected_dataset)

if __name__ == "__main__":

    # Config
    directory = "data/mathcomp"
    scorer = "bm25"
    selector = "100_900"
    model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
    vllm_address = "http://localhost:8000/v1"
    prompter = proof_prompter.prompter

    make(directory, scorer, selector, model, vllm_address, prompter)
