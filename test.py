from modules import urlFactory

DEBUG_MODE = True

#
urlFactory._fetchCCTVList(DEBUG_MODE=DEBUG_MODE)
#
#urlFactory._getCCTVNameList(DEBUG_MODE=DEBUG_MODE, mode="tag")
#
#print(urlFactory._getCCTVUrl(DEBUG_MODE=DEBUG_MODE, cctvName=""))

urlFactory.showAllCCTVs(DEBUG_MODE=DEBUG_MODE, mode='name')