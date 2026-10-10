import asyncio
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from atguigu.domain.state import DialogueState
from atguigu.repository.models.dialogue_state import DialogueStateRecord
from atguigu.infrastructure import database


class DialogueStateRepository:

    def __init__(self,session:AsyncSession):
        self._session = session

    async def load(self,sender_id:str)->DialogueState:
        # select * from dialogue_state where sender_id = u1001
        result = await self._session.execute(
            select(DialogueStateRecord).where(DialogueStateRecord.sender_id == sender_id)
        )
        # 基于0RM类， 构造—个select语句: select sender_id,state_json from dialogue_states where sender_id = 'u1001'
        # 从结果中获取记录
        record = result.scalar_one_or_none()
        if record is None:
            return DialogueState(sender_id)
        #如果record有值
        json_str = record.state_json
        dict_data = json.loads(json_str)
        return DialogueState.from_dict(dict_data)

    async def save(self,state:DialogueState)->None:
        """
        更新对话状态
        """
        #1.将state转化为json字符串
        json_str = json.dumps(state.to_dict(),ensure_ascii=False)
        #2. 根据state.sender_id查询用户状态
        result = await self._session.execute(
            select(DialogueStateRecord).where(DialogueStateRecord.sender_id == state.sender_id)
        )
        record = result.scalar_one_or_none()
        #3. 判断用户状态
        if record is None:
            #   如果没有查询到结果，则插入新用户状态
            self._session.add(
                DialogueStateRecord(
                    sender_id = state.sender_id,state_json=json_str
                )
            )
        else:
            #   如果查询到了结果，则更新
            record.state_json = json_str
        await self._session.commit()

if __name__ == "__main__":
    database.init_db_engine_and_session_factory()

    async def test():
        async with database.session_factory() as session:
            repo = DialogueStateRepository(session)
            record = await repo.load("u1003")
            print("查询结果:", record)

        await database.close_db_engine()

    asyncio.run(test())