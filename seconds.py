from kivy.clock import Clock
from kivy.uix.label import Label

class Seconds(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seconds = 0
        self.running = False
        self._clock_event = None
        self.text = '00:00'
        self.finish_callback = None
    
    def start(self, total_seconds, finish_callback=None):
        self.stop()
        self.seconds = total_seconds
        self.running = True
        self.finish_callback = finish_callback
        self._update_text()
        self._clock_event = Clock.schedule_interval(self._update, 1)
    
    def stop(self):
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None
        self.running = False
    
    def _update(self, dt):
        if self.seconds > 0:
            self.seconds -= 1
            self._update_text()
            return True
        else:
            self.running = False
            if self.finish_callback:
                self.finish_callback()
            return False
    
    def _update_text(self):
        minutes = self.seconds // 60
        secs = self.seconds % 60
        self.text = f"{minutes:02d}:{secs:02d}"