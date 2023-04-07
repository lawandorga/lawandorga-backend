from typing import Any, Optional

from core.seedwork.aggregate import Addon, Aggregate
from messagebus import Event, MessageBus
from messagebus.domain.data import JsonDict


class Object(Aggregate):
    uuid: Any


class EventsAddon(Addon):
    def __init__(self, obj: Object):
        super().__init__(obj)
        self.__raw_events: list[Event] = []
        self.__events: list[Event] = []

    def __save(self) -> None:
        for raw_event in self.__raw_events:
            event = MessageBus.save_event(raw_event)
            self.__events.append(event)

        self.__raw_events = []

    def __handle(self) -> None:
        for event in self.__events:
            MessageBus.handle(event)

        self.__events = []

    def add(self, event: Event, metadata: Optional[JsonDict] = None):
        event.set_aggregate_uuid(self._obj.uuid)
        self.__raw_events.append(event)

    on_save = [__save]
    on_delete = [__save]
    post_save = [__handle]
    post_delete = [__handle]
