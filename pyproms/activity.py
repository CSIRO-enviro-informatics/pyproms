from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import RDF, RDFS
import datetime
from pyproms.rdfclass import RdfClass
from pyproms.entity import Entity
from pyproms.agent import Agent


# Todo: change to like Entity
# TODO: allow Activity - Activity relationships
class Activity(RdfClass):
    def __init__(self,
                 prov_or_proms,
                 label,
                 uri=None,
                 wasAssociatedWith=None,
                 startedAtTime=None,
                 endedAtTime=None,
                 comment=None,
                 used_entities=None,
                 generated_entities=None,
                 wasInformedBy=None):

        RdfClass.__init__(self, label, uri, comment)

        self.prov_or_proms = prov_or_proms
        self.wasAssociatedWith = wasAssociatedWith
        self.startedAtTime = startedAtTime
        self.endedAtTime = endedAtTime
        self.used_entities = used_entities
        if used_entities:
            self.set_used_entities(used_entities)
        else:
            self.used_entities = None
        if generated_entities:
            self.set_generated_entities(generated_entities)
        else:
            self.generated_entities = None
        self.wasInformedBy = wasInformedBy

    def set_wasAssociatedWith(self, wasAssociatedWith):
        if type(wasAssociatedWith) is Agent:
            self.wasAssociatedWith = wasAssociatedWith
        else:
            raise TypeError('wasAssociatedWith must be an Agent, not a %s' % type(wasAssociatedWith))

    def set_startedAtTime(self, startedAtTime):
        if type(startedAtTime) is datetime.datetime:
            self.startedAtTime = startedAtTime
        else:
            raise TypeError('startedAtTime must be a datetime.datetime, not a %s' % type(startedAtTime))

    def set_endedAtTime(self, endedAtTime):
        if type(endedAtTime) is datetime.datetime:
            self.startedAtTime = endedAtTime
        else:
            raise TypeError('endedAtTime must be a datetime.datetime, not a %s' % type(endedAtTime))

    def set_used_entities(self, used_entities):
        if all(isinstance(n, Entity) for n in used_entities):
            self.used_entities = used_entities
        else:
            raise TypeError('used_entities must be a list of Entity objects')

    def set_generated_entities(self, generated_entities):
        if all(isinstance(n, Entity) for n in generated_entities):
            self.used_entities = generated_entities
        else:
            raise TypeError('used_entities must be a list of Entity objects')

    def set_wasInformedBy(self, wasInformedBy):
        self.wasInformedBy = wasInformedBy

    def make_graph(self):
        RdfClass.make_graph(self)

        PROV = Namespace('http://www.w3.org/ns/prov#')
        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        PROMS = Namespace('http://promsns.org/def/proms#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROV.Activity))

        # TODO: add Activity to PROMS-O
        if self.prov_or_proms == 'PROMS':
            self.g.add((URIRef(self.uri),
                        RDF.type,
                        PROMS.Activity))

        if self.wasAssociatedWith:
            self.g.add((URIRef(self.uri),
                        PROV.wasAssociatedWith,
                        URIRef(self.wasAssociatedWith)))

        if self.startedAtTime:
            self.g.add((URIRef(self.uri),
                        PROV.startedAtTime,
                        URIRef(self.startedAtTime)))

        if self.endedAtTime:
            self.g.add((URIRef(self.uri),
                        PROV.endedAtTime,
                        URIRef(self.endedAtTime)))

        if self.used_entities:
            for used_entity in self.used_entities:
                #add the Entity to the graph
                self.g = self.g + used_entity.get_graph()
                #associate the Entity with the Activity
                self.g.add((URIRef(self.uri),
                            PROV.used,
                            URIRef(used_entity.uri)))

        if self.generated_entities:
            for generated_entity in self.generated_entities:
                #add the Entity to the graph
                self.g = self.g + generated_entity.get_graph()
                #associate the Entity with the Activity
                self.g.add((URIRef(self.uri),
                            PROV.generated,
                            URIRef(generated_entity.uri)))

        if self.wasInformedBy:
            self.g.add((URIRef(self.uri),
                        PROV.wasInformedBy,
                        URIRef(self.wasInformedBy)))

    def get_graph(self):
        """
        Generates the RDF graph of this class

        :return: This class's RDF graph
        """
        if not self.g:
            self.make_graph()

        return self.g