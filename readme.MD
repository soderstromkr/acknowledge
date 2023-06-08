#readme

## Code description
Code for paper : "Who did what? : Creating structured data   from acknowledgement texts with large language models".  

## Use
The code and completions are optimized for the data used in this article. If you want to use it for your data:
1. Add your OpenAI key in the file 'secret_key.py'.
2. Add your own completions in the file 'completions.py'. The code is divided into three sections: keys, few shot learning mapping and instructions.
    a. Keys tells the model which elements you want to extract with either method: few-shot or instruction. 
    b. Few-show learning requires mapping prompts to completions. In this case, acknowledgements texts were mappped with outputs in JSON format. 
    c. Instruction requires a natural language instruction to run.
You can modify these, as long as you keep a similar formatting to the original.

## Defaults
Model has a few default values to keep in mind:
1. max_tokens = max tokens to generate (set to 500)
2. stop = sequence where API will stop generating. (None for instructions, '\n\n[Output]:' for few-shot)
3. temperature = level of randomness in the model (set to 0)
