# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *


@plugins.register(
    name="Diet",
    desire_priority=100,
    desc="A plugin that use LLM to determine user diet is healthy or not",
    version="0.1",
    author="william Jin",
)
class Diet(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[Intent] inited")
        # self.config = super().load_config()
        

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT,
            ContextType.IMAGE
        ]:
            return
        if e_context["context"].type == ContextType.IMAGE:
            # TODO:调用LLM识别图片中的食物
            content = self.get_image_food(e_context["context"].content)
            # TODO:调用LLM获取饮食建议
            suggestion = self.get_suggestion(content)
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = suggestion
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 返回饮食建议，并终止后续处理
        else:
            intent = e_context["intent"]
            if intent != '饮食':
                return
            else:
                # TODO: 调用LLM获取饮食建议
                pass
        
    def get_image_food(self, content):
        return "奶油蛋糕"
    
    def get_suggestion(self, content):
        return "建议少吃"
        