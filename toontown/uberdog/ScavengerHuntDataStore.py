from direct.directnotify import DirectNotifyGlobal
from toontown.uberdog.DataStore import *

import json

class ScavengerHuntDataStore(DataStore):
    QueryTypes = DataStore.addQueryTypes(['GetGoals', 'AddGoal'])
    notify = DirectNotifyGlobal.directNotify.newCategory('ScavengerHuntDataStore')

    def __init__(self, filepath):
        DataStore.__init__(self, filepath)

    def handleQuery(self, query):
        qId, qData = query
        if qId == self.QueryTypes['GetGoals']:
            avId, goal = qData
            goals = self.__getGoalsForAvatarId(avId)
            return (qId, (avId, goal, goals))
        elif qId == self.QueryTypes['AddGoal']:
            avId, goal = qData
            self.__addGoalToAvatarId(avId, goal)
            return (qId, (avId,))
        return None

    def __addGoalToAvatarId(self, avId, goal):
        if self.wantAnyDbm:
            pAvId = json.dumps(avId)
            pGoal = json.dumps(goal)
            pData = self.data.get(pAvId, None)
            if pData is not None:
                data = json.loads(pData)
            else:
                data = set()
            data.add(goal)
            pData = json.dumps(data)
            self.data[pAvId] = pData
        else:
            self.data.setdefault(avId, set())
            self.data[avId].add(goal)
        self.incrementWriteCount()
        return

    def __getGoalsForAvatarId(self, avId):
        if self.wantAnyDbm:
            pAvId = json.dumps(avId)
            pData = self.data.get(pAvId, None)
            if pData is not None:
                data = list(json.loads(pData))
            else:
                data = []
            return data
        else:
            return list(self.data.get(avId, []))
        return
