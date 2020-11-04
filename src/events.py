class EventManager():
    def __init__(self):
        self.handlers = {}

    def on(self, eventName: str, callback: callable) -> None:
        if eventName not in self.handlers:
            self.handlers[eventName] = []
        if callback in self.handlers[eventName]:
            raise BaseException(
                f"Cannot have duplicate callback in EventManager for event {eventName}!")
        self.handlers[eventName].append(callback)

    def remove_on(self, eventName: str, callback: callable) -> None:
        if eventName not in self.handlers:
            return
        self.handlers[eventName].remove(callback)

    def emit(self, eventName, *args) -> None:
        # print(f"EMITTING {eventName}")
        if eventName not in self.handlers:
            return
        for callback in self.handlers[eventName]:
            callback(*args)
