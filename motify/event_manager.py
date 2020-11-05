class EventManager():
    """A simple event manager used for emitting events.
    """

    def __init__(self):
        """Initialize with no events or handlers.
        """
        self.handlers = {}

    def on(self, eventName: str, callback: callable) -> None:
        """When eventName happens, call the callback function.

        Args:
            eventName (str): the event to track
            callback (callable): the callback to call

        Raises:
            BaseException: duplicate callbacks registered
        """
        if eventName not in self.handlers:
            self.handlers[eventName] = []
        if callback in self.handlers[eventName]:
            raise BaseException(
                f"Cannot have duplicate callback in EventManager for event {eventName}!")
        self.handlers[eventName].append(callback)

    def remove_on(self, eventName: str, callback: callable) -> None:
        """Removes a callback from an event.

        Args:
            eventName (str): the event the callback is in
            callback (callable): the callback to remove
        """
        if eventName not in self.handlers:
            return
        self.handlers[eventName].remove(callback)

    def emit(self, eventName: str, *args) -> None:
        """Emits the specified event with any args.

        Args:
            eventName (str): the event to emit to listeners
        """
        if eventName not in self.handlers:
            return
        for callback in self.handlers[eventName]:
            callback(*args)
