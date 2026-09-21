import sys

from botocore.exceptions import BotoCoreError, ClientError

from bedrock_client import build_agent


def main() -> int:
    print("Simple Strands + Bedrock chat")
    print("Type 'exit' or 'quit' to stop.\n")

    try:
        agent = build_agent()
    except Exception as exc:
        print(f"Failed to initialize Bedrock agent: {exc}", file=sys.stderr)
        return 1

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return 0

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            return 0

        if not user_input:
            continue

        try:
            response = agent(user_input)
        except (BotoCoreError, ClientError) as exc:
            print(f"Bedrock request failed: {exc}", file=sys.stderr)
            continue
        except Exception as exc:
            print(f"Unexpected error: {exc}", file=sys.stderr)
            continue

        print(f"Assistant: {response}\n")


if __name__ == "__main__":
    raise SystemExit(main())
