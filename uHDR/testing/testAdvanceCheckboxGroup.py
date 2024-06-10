from guiQt.AdvanceCheckBoxGroup import AdvanceCheckBoxGroup

def test() -> AdvanceCheckBoxGroup:
    
    advCBG : AdvanceCheckBoxGroup = AdvanceCheckBoxGroup(
        {
            ("type0","name00"):True,
            ("type0","name01"):True,
            ("type0","name02"):True,
            ("type1","name10"):True,
            ("type1","name11"):True
        }) 
    # advSlider.valueChanged.connect(lambda x,y: print(f'valueChanged({x},{y})'))
    # advSlider.autoClicked.connect(lambda :print(f'autoClicked({"."})'))
    # advSlider.activeToggled.connect(lambda x :print(f'autoClicked({x})'))

    return advCBG