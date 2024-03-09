from typing import Callable
from pygame import event

from .utils import Singleton


class EventManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.subscribers: dict[int, list[Callable]] = {}
        self.frame_events: list[event.Event] = []

    def process_events(self) -> None:
        self.frame_events = event.get()
        for ev in self.frame_events:
            if not ev.type in self.subscribers.keys():
                continue
            for callback in self.subscribers.get(ev.type):
                callback(ev)
    
    def subscribe(self, event_type: int, callback: Callable) -> None:
        if not event_type in self.subscribers.keys():
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: int, callback: Callable) -> None:
        self.subscribers.get(event_type).remove(callback)
    
    def get_events(self, event_type: int) -> list[event.Event] | list:
        return [ev for ev in self.frame_events if ev.type == event_type]
