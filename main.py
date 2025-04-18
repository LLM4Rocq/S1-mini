import score_dataset, select_dataset, chain_of_thought
import proof_prompter, proof_mapping_prompter

def make(dataset, scorer, selector, model, vllm_address, prompter):
    data_info = score_dataset.make(dataset, scorer)
    data_info = select_dataset.make(selector, data_info)
    return chain_of_thought.make(model, vllm_address, prompter, data_info)

if __name__ == "__main__":

    # Config
    dataset = "mathcomp"
    scorer = "bm25"
    selector = "q9_1000"
    model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
    vllm_address = "http://localhost:8000/v1"
    prompter = proof_prompter.prompter

    make(dataset, scorer, selector, model, vllm_address, prompter)
