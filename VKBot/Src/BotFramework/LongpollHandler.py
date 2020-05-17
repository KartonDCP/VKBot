import inspect

from vk_api import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from Src.BotFramework.EventSender import ChatEventSender
from Src.BotFramework.VkAction import VkAction
from Src.Controllers.ChatMsgController import ChatMsgController


class LongPollHandler:

    def __init__(self, token: str):
        self._vk_session = vk_api.VkApi(token=token)
        self._session_api = self._vk_session.get_api()
        self._long_poll = VkLongPoll(self._vk_session)
        self._vk_action = VkAction(token)

        self.chat_controller = ChatMsgController(self._vk_action)

        self.chat_handlers = self._methods_with_decorator(ChatMsgController, "HandleMessage")

    async def callback_listener(self):
        pass

    def start_handle(self):
        for event in self._long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.from_chat:
                    print(event.text)
                    # trying find handler for message
                    for handler in self.chat_handlers:
                        msg_handle = handler[1].split('=')[1].replace('\"', '').replace(' ', '').replace('\'', '')
                        if msg_handle == event.text:
                            chat_event = ChatEventSender(event.chat_id,
                                                         int(event.extra_values['from']),
                                                         {"message": event.text,
                                                          "attachment": event.attachments})
                            getattr(self.chat_controller, handler[0])(chat_event)   # Call method by name
                if event.from_user:
                    pass    # ChatController Startup
                if event.from_group:
                    pass
                if event.from_me:
                    pass

    def _find_def_with(self, msg: str, decorator: str, controller_name: str):
        pass

    @staticmethod
    def _methods_with_decorator(controller_name, decorator_name: str) -> list:
        # raise Warning("\"_methods_with_decorator\" Method works with errors! do unit tests and rewrite it")
        source_lines = inspect.getsourcelines(controller_name)[0]
        result = []
        for i, line in enumerate(source_lines):
            line = line.strip()
            if line.split('(')[0].strip() == '@' + decorator_name:
                param = line.split('(')[1].split(')')[0]
                next_line = source_lines[i + 1]
                while '@' in next_line:
                    next_line = source_lines[i+1]
                decor_name = next_line.split('def')[1].split('(')[0].strip()
                item = (decor_name, param)
                result.append(item)
        return result

    def load_stateless_controllers(self, typename: str) -> list:
        pass

longpoll = LongPollHandler('cdefe64cad4dfb777159fed5802a6a85ddc7a29eaa4e7f6e876096a07ce53887baa982487b8883b964f8d')
longpoll.start_handle()


