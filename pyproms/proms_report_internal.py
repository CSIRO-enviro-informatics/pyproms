from rdflib import URIRef, Namespace
from rdflib.namespace import RDF
from pyproms.proms_report import PromsReport
from pyproms.prov_activity import ProvActivity
from pyproms.proms_error import *


class PromsInternalReport(PromsReport):
    """
    Creates a PROMS-O Internal Report instance
    
    This has the set of all Activities and an ending activity in addition to a Report class object
    """
    def __init__(self,
                 label,
                 wasReportedBy,
                 nativeId,
                 startingActivity,
                 endingActivity,
                 all_activities,
                 generatedAtTime,
                 comment=None):
        
        PromsReport.__init__(self,
                             label,
                             wasReportedBy,
                             nativeId,
                             startingActivity,
                             generatedAtTime,
                             comment)

        self.__set_endingActivity(startingActivity, endingActivity)
        self.__set_all_activities(all_activities)

    def __set_endingActivity(self, startingActivity, endingActivity):
        if type(endingActivity) is ProvActivity:
            if startingActivity is not None:
                if endingActivity == startingActivity:
                    raise PromsOntologyError(
                        'For an Internal Report, the ending activity and starting activity must not be the same')
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
        self.g.bind('proms', PROMS)

        self.g.remove((
            URIRef(self.uri),
            RDF.type,
            PROMS.Report))
        self.g.add((
            URIRef(self.uri),
            RDF.type,
            PROMS.InternalReport))

        for activity in self.all_activities:
            # add the Activity to the graph
            self.g = self.g + activity.get_graph()

        # remove the triple that points the endingActivity to the startingActivity in the Report class
        self.g.remove((None, PROMS.endingActivity, None))
        # re-add the endingActivity triple pointing to the new Activity
        self.g.add((URIRef(self.uri),
                    PROMS.endingActivity,
                    URIRef(self.endingActivity.uri)))
