from transducer import *

# DEFAULT_TRANSDUCER = HaskellTrans
DICT_TRANSDUCER = {"QTree": QTreeTrans, "Haskell": HaskellTrans, "Forest": ForestTrans}
DEFAULT_TRANSDUCER = QTreeTrans
SPROUT_DIST = 20.
POS_ABS_ROOT = (0, 80)
EXPONENT = 1.1