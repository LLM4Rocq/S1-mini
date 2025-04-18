from openai import OpenAI
import os
import json
from datetime import datetime
from tqdm import tqdm

class Prompter():
    def __init__(self, sys_prompt, usr_prompt, parse, format):
        self.sys_prompt = sys_prompt
        self.usr_prompt = usr_prompt
        self.parse = parse
        self.format = format

    def prompt(self, theorem):
        return [
            { "role": "system", "content": self.sys_prompt },
            { "role": "user", "content": self.usr_prompt.format(**theorem) }
        ]

def log(logfile, messages: list[str], resp: str):
    with open(logfile, "a") as file:
        content = {
            "message": "\n".join([m["content"] for m in messages]),
            "response": resp
        }
        content = json.dumps(content, indent=2)
        file.write(content + "\n")

def response(client, model, temperature, logger, messages: list[str]) -> str:
    raw = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=4096,
        temperature=temperature
    )
    resp = raw.choices[0].message.content
    logger(messages, resp)
    return resp

def make(model, vllm_address, prompter, datafile, temperature=1.0):
    """Add chains of thought to a dataset of theorems."""

    dt = datetime.now().strftime("%y%m%d_%H%M%S")

    provider, model_name = model.split('/')
    datafilename = os.path.splitext(datafile)[0]
    savefile = f"{datafilename}_{provider}_{model_name}_{dt}.jsonl"

    if os.path.exists(savefile):
        print("Chains of Thought already available ...")
    else:

        print("  Reading the data ...")
        thms = []
        with open(datafile, "r") as datas:
            for i, thm in enumerate(datas):
                if i % 4 == 0:
                    thms.append(thm)
                else:
                    thms[i//4] += "\n" + thm

        client = OpenAI(
            api_key="EMPTY",
            base_url=vllm_address
        )

        datafilename = os.path.basename(datafilename)
        logfile = os.path.join("./log", f"{datafilename}_{provider}_{model_name}_{dt}")
        open(logfile, "w").close()
        def logger(messages, response):
            log(logfile, messages, response)

        print("  Generating chains of thought ...")
        with open(savefile, "w") as new_datas:
            for thm in tqdm(thms):
                thm = json.loads(thm)
                messages = prompter.prompt(thm)
                resp = response(client, model, temperature, logger, messages)
                llm_result = prompter.parse(resp)
                result = prompter.format(thm, llm_result)

                result = json.dumps(result, indent=2)
                new_datas.write(result + "\n")

        print("  DONE!")

    return savefile
