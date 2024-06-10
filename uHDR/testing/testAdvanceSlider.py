from guiQt.AdvanceSlider import AdvanceSlider

def test() -> AdvanceSlider:
    
    advSlider : AdvanceSlider = AdvanceSlider('test:slider', 5, (0,20), (0,10),10)
    advSlider.valueChanged.connect(lambda x,y: print(f'valueChanged({x},{y})'))
    advSlider.autoClicked.connect(lambda :print(f'autoClicked({"."})'))
    advSlider.activeToggled.connect(lambda x :print(f'autoClicked({x})'))

    return advSlider