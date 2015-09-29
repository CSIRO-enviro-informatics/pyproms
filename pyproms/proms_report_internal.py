from rdflib import URIRef, Namespace
from rdflib.namespace import RDF
from pyproms.proms_report import PromsReport
from pyproms.prov_activity import ProvActivity
from pyproms.proms_activity import PromsActivity
from proms_error import PromsDataModelError


class PromsInternalReport(PromsReport):
    """
    Creates a PROMS-O Basic Report instance
    
    This has no new features on top of Report but it's worth maintaining the separate classes
    """
    def __init__(self,
                 label,
                 reportingSystem,
                 nativeId,
                 startingActivity,
                 endingActivity,
                 all_activities,
                 comment=None):
        
        PromsReport.__init__(self,
                             label,
                             reportingSystem,
                             nativeId,
                             comment)

        self.__set_startingActivity(startingActivity)
        self.__set_endingActivity(endingActivity)
        self.__set_all_activities(all_activities)

    def __set_startingActivity(self, startingActivity):
        if (type(startingActivity) is ProvActivity or
            type(startingActivity) is PromsActivity):
            # TODO: enable this check
            #if endingActivity is not None:
            #    if startingActivity == endingActivity:
            #        raise PromsDataModelError('For an Internal Report, the starting activity and ending activity must not be the same')
            self.startingActivity = startingActivity
        else:
            raise TypeError('startingActivity must be an Agent, not a %s' % type(startingActivity))

    def __set_endingActivity(self, endingActivity):
        if (type(endingActivity) is ProvActivity or
            type(endingActivity) is PromsActivity):
            if self.startingActivity is not None:
                if endingActivity == self.startingActivity:
                    raise PromsDataModelError('For an Internal Report, the ending activity and starting activity must not be the same')
            self.endingActivity = endingActivity
        else:
            raise TypeError('endingActivity must be an Agent, not a %s' % type(endingActivity))

    def __set_all_activities(self, all_activities):
        if all(isinstance(n, ProvActivity) for n in all_activities):
            self.all_activities = all_activities
        else:
            raise TypeError('all_activities must be a list of Activity objects')

    def make_graph(self):
        """
        Specialises PromsReport.make_graph()

        :return: an rdflib Graph object
        """
        PromsReport.make_graph(self)

        PROMS = Namespace('http://promsns.org/def/proms#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROMS.InternalReport))
        
        self.g = self.g + self.startingActivity.get_graph()
        self.g.add((URIRef(self.uri),
                    PROMS.startingActivity,
                    URIRef(self.startingActivity.uri)))

        self.g = self.g + self.endingActivity.get_graph()
        self.g.add((URIRef(self.uri),
                    PROMS.endingActivity,
                    URIRef(self.endingActivity.uri)))

        for activity in self.all_activities:
            # add the Activity to the graph
            self.g = self.g + activity.get_graph()