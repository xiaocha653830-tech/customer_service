import importlib
import inspect
import pkgutil

from task.action.base import Action
from task.action.builtin.action_listen import ActionListen
from task.action.builtin.action_response import ActionResponse
from task.action.registry import ActionRegistry
from task.action.runner import ActionRunner


def registry_custom_actions(registry:ActionRegistry):
    #完成自定义Action类的注册
    # 1.导入atguigu.task.action.custom包
    package = importlib.import_module("atguigu.task.action.custom")
    # 2.遍历包中所有模块
    for __,name,is_pkg in pkgutil.iter_modules(package.__path__,prefix=package.__name__+"."):
        if is_pkg:
            continue
        # 导入包中模块
        module = importlib.import_module(name)
        # 3.获取模块中的所有类
        for __,obj in inspect.getmembers(module,inspect.isclass):
            # 如果模块中的类是Action的子类，但不是Action类本身，则进行注册
            if not issubclass(obj,Action) and obj is not Action:
                registry.register( obj() )


def build_action_runner()->ActionRunner:
    registry = ActionRegistry()
    #使用静态方法注册内置Action
    registry.register( ActionResponse() )
    registry.register( ActionListen() )
    #注册自定义Action(通过扫描包来完成自定义Action的注册)
    registry_custom_actions(registry)

    return ActionRunner(registry)