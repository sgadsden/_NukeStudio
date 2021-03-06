import nuke
from _pkg_KuFunc import *
from _pkg_Studios import *
from _mod_Download import *

from _pkg_KuFunc.mod_KuUtility import *



########## DEFAULT NODE VALUE ##########




nuke.knobDefault('Blur.size', '12')
nuke.knobDefault('Blur.channels', 'alpha')

nuke.knobDefault('FilterErode.channels', 'alpha')
nuke.knobDefault('FilterErode.filter', 'gaussian')
nuke.knobDefault('Dilate.channels', 'alpha')
nuke.knobDefault('Defocus.channels', 'alpha')

nuke.knobDefault('OFXuk.co.thefoundry.keylight.keylight_v201.show', 'Intermediate Result')

nuke.knobDefault('Denoise.amount','.5')
nuke.knobDefault('Denoise.lumaAmount','4.5')

nuke.knobDefault('Remove.operation', 'keep')
nuke.knobDefault('Remove.channels', 'rgba')
nuke.knobDefault('Remove.label', '[value channels]')

nuke.knobDefault('Switch.which', '1')
nuke.knobDefault('Switch.label', '[value which]')

nuke.knobDefault('Log2Lin1.label', '[value operation]')
nuke.knobDefault('Log2Lin1.operation', 'lin2log')
nuke.knobDefault('OCIOLogConvert.label', '[value operation]')
nuke.knobDefault('OCIOLogConvert.operation', 'lin2log')

nuke.knobDefault('StickyNote.note_font', 'bold')
nuke.knobDefault('StickyNote.note_font_size', '24')

nuke.knobDefault('Multiply.label', '[value value]')
nuke.knobDefault('Expression.label', 'a::[value expr3]')
nuke.knobDefault('Invert.channels', 'alpha')
nuke.knobDefault('IBKColourV3.Size', '1')
nuke.knobDefault('Shuffle.label', '[value in]')
nuke.knobDefault('Roto.cliptype', 'no clip')
nuke.knobDefault('Rotopaint.cliptype', 'no clip')
nuke.knobDefault('Constant.channels', 'rgba')
nuke.knobDefault('Constant.color', '0.18 0.18 0.18 1.0')

### Viewer Node ###
nuke.knobDefault('Viewer.frame_increment', '8')
nuke.knobDefault('Viewer.hide_input', 'True')




########## Nuke OnStartUp ##########
# nuke.addOnUserCreate(function, nodeClass='Class')
# nuke.addOnCreate(mod_StudioENV.StudioENV, nodeClass='Root')

def viewerSetting():
    for n in nuke.allNodes('Viewer'):
        n['frame_increment'].setValue(8)
        n['hide_input'].setValue(True)

nuke.addOnCreate(viewerSetting, nodeClass='Root')
