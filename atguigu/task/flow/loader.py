from pathlib import Path
import yaml
from task.flow.models import FlowList, FlowSlot, Flow, FlowStep, CollectFlowStep


class FlowLoader:

    def load_many(self,paths:list[Path])->FlowList:
        slots = {}
        flows = []
        for path in paths:
            flowslist = self.load(path)
            slots.update(flowslist.slots)
            flows.extend(flowslist.flows)
        return FlowList(slots=slots, flows=flows)

    def load(self,path:Path)->FlowList:
        with open(path,'r',encoding="utf-8") as file:
            data = yaml.safe_load(file)
            # 获取yml文件中的slots数据
            slots_data = data.get('slots',{})
            # 解析slots数据
            slots = self._load_slots(slots_data)
            # 获取yml文件中的flows数据
            flows_data = data.get('flows')
            # 解析flows数据
            flows = self._load_flows(flows_data,slots)

            return FlowList(
                slots=slots,
                flows=[]
            )

    def _load_slots(self,slots_data:dict)->dict[str,FlowSlot]:
        slots = {}
        for slot_name , slots_data in slots_data.items():
            slots[slot_name] = FlowSlot(
                name=slot_name,
                type=slots_data.get('type'),
                label=slots_data.get('label'),
                description=slots_data.get('description'),
            )
        return slots

    def _load_flows(self,flows_data:dict,slots:dict[str,FlowSlot])->list[Flow]:
        flows = []
        for flow_id,flow_data in flows_data.items():
            flow_name = flow_data.get('name')
            flow_description = flow_data.get('description')
            steps = [FlowStep.from_dict(step_data) for step_data in flow_data.get('steps')]
            flow_slots = []
            for step in steps:
                if isinstance(step,CollectFlowStep):
                    flow_slot:FlowSlot = slots.get(step.slot_name)
                    flow_slots.append(flow_slot)

            flows.append(Flow(
                id=flow_id,
                name=flow_name,
                description=flow_description,
                steps=steps,
                slots=flow_slots
            ))
        return flows