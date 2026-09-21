import os

from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

load_dotenv()


def build_agent() -> Agent:
    model_id = os.getenv("BEDROCK_MODEL_ID",
                         "anthropic.claude-3-5-sonnet-20240620-v1:0")
    region = os.getenv("AWS_REGION") or os.getenv(
        "AWS_DEFAULT_REGION") or "us-east-1"

    model = BedrockModel(model_id=model_id, region_name=region)
    return Agent(model=model)
