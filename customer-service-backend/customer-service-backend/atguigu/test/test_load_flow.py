from pathlib import Path

from task.flow.loader import FlowLoader

if __name__ == '__main__':
    user_flows_path = Path(__file__).parents[2]/'flowConfig'/'user_flows.yml'
    system_flows_path = Path(__file__).parents[2]/'flowConfig'/'system_flows.yml'
    load = FlowLoader()
    flows_list = load.load_many([user_flows_path, system_flows_path])
    print(flows_list)
