def _version_():
	ver='''

	version 0
	- Toggle between $GUI and no $GUI
	- Suggested shortkey: "shift+d", "shift+alt+d"
	'''




import nuke



def GUISwitch(mode='switch'):

  	'''
  	- mode='switch': add $gui if none, remove if do
  	- mode='reverse': revserse $gui if !$gui, also add $gui if none
  	'''

  	nodes = nuke.selectedNodes()

	def setGUI():
		if knob.hasExpression() and "$gui" in knob.toScript():
			knob.clearAnimated()
			knob.setValue(False)
		else:
			knob.setExpression('$gui')

	for n in nodes:
		knob = n.knob('disable')

	if mode=='switch':
		setGUI()
	if mode=='reverse':
		if knob.hasExpression() and "!" in knob.toScript():
			knob.setExpression('$gui')
		else:
			knob.setExpression('!$gui')
