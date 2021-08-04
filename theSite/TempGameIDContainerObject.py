class TempGameIDContainerObject:

    def __init__(self):
        self._iGDBgameID = None
        self._iGDBHeaders = None
        self._iGDBName = None
        self._steamGameID = None


    @property
    def iGDBgameID(self):
        return self._iGDBgameID

    @property
    def steamGameID(self):
        return self._steamGameID

    @property
    def iGDBName(self):
        return self._iGDBName

    @property
    def iGDBHeaders(self):
        return self._iGDBHeaders

    @iGDBgameID.setter
    def iGDBgameID(self, igdbGameVal):
        self._iGDBgameID = igdbGameVal

    @iGDBName.setter
    def iGDBName(self, gameName):
        self._iGDBName = gameName

    @steamGameID.setter
    def steamGameID(self, steamIDval):
        self._steamGameID = steamIDval

    @iGDBHeaders.setter
    def iGDBHeaders(self, igdbHeadersVal):
        self._iGDBHeaders = igdbHeadersVal