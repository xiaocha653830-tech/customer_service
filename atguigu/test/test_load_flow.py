from pathlib import Path

from task.flow.loader import FlowLoader

if __name__ == '__main__':
    user_flows_path = Path(__file__).parents[2]/'flowConfig'/'user_flows.yml'
    print(user_flows_path)
    # loader = FlowLoader()
    # loader.load()