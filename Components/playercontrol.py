from .base import Base

class PlayerControl(Base):
    def __init__(self):
        super().__init__()
    def test_func(self):
        print(f"successfully called the test function of {self} from {self.parent}")