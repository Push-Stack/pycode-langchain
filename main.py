from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
from dotenv import load_dotenv
import argparse

load_dotenv()

parser = argparse.ArgumentParser()

parser.add_argument('--language', default='Python')
parser.add_argument(
    '--task', default='Write a program that takes two numbers as input and calculates their sum.')

args = parser.parse_args()

llm = OpenAI()

# Template
chat_template = PromptTemplate(
    input_variables=['language', 'task'],
    template='Write code in {language}. Your task is to: \n${task}'
)
# 1st Chain
chat_chain = LLMChain(
    llm=llm,
    prompt=chat_template,
    output_key='code'
)

# Template
test_code_template = PromptTemplate(
    input_variables=['language', 'code'],
    template='Write a test for the following {language} code: \n${code}'
)

# 2nd Chain
test_chain = LLMChain(
    prompt=test_code_template,
    llm=llm,
    output_key='test'
)

chains = SequentialChain(
    chains=[chat_chain, test_chain],
    input_variables=['language', 'task'],
    output_variables=['code', 'test']
)

result = chat_chain.invoke({
    'language': args.language,
    'task': args.task
})

print(result)
