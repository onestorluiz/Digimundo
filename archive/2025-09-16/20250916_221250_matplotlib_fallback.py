
# Fallback implementation for matplotlib when not available
class MockPlot:
    def figure(self, *args, **kwargs):
        return MockFigure()

    def subplots(self, *args, **kwargs):
        return MockFigure(), MockAxes()

    def show(self):
        pass

    def savefig(self, *args, **kwargs):
        pass

class MockFigure:
    def suptitle(self, *args, **kwargs):
        pass

class MockAxes:
    def plot(self, *args, **kwargs):
        pass

    def bar(self, *args, **kwargs):
        pass

    def set_title(self, *args, **kwargs):
        pass

    def set_xlabel(self, *args, **kwargs):
        pass

    def set_ylabel(self, *args, **kwargs):
        pass

pyplot = MockPlot()
plt = pyplot
