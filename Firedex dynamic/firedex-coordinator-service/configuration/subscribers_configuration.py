
from model.network_flow_collection import NetworkFlowCollection

class SubscribersConfiguration:

    def __init__(self):
        self.__network_flow_collection = NetworkFlowCollection()

    def network_flow_collection(self):
        return self.__network_flow_collection
