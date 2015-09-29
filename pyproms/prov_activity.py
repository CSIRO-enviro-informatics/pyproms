from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF
import datetime
from pyproms.owlclass import OwlClass
from pyproms.prov_entity import ProvEntity
from pyproms.prov_agent import ProvAgent


class ProvActivity(OwlClass):
    """
    Creates a PROV-O Activity instance
    """
    def __init__(self,
                 label,
                 startedAtTime,
                 endedAtTime,
                 uri=None,
                 wasAssociatedWith=None,
                 comment=None,
                 used_entities=None,
                 generated_entities=None,
                 wasInformedBy=None):

        OwlClass.__init__(self, label, uri, comment)

        self.set_startedAtTime(startedAtTime)
        self.set_endedAtTime(endedAtTime)

        if wasAssociatedWith:
            self.set_wasAssociatedWith(wasAssociatedWith)
        else:
            self.wasAssociatedWith = None

        if used_entities:
            self.set_used_entities(used_entities)
        else:
            self.used_entities = None

        if generated_entities:
            self.set_generated_entities(generated_entities)
        else:
            self.generated_entities = None

        if wasInformedBy:
            self.set_wasInformedBy(wasInformedBy)
        else:
            self.wasInformedBy = None

    def set_wasAssociatedWith(self, wasAssociatedWith):
        if type(wasAssociatedWith) is ProvAgent:
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
            self.endedAtTime = endedAtTime
        else:
            raise TypeError('endedAtTime must be a datetime.datetime, not a %s' % type(endedAtTime))

    def set_used_entities(self, used_entities):
        if all(isinstance(n, ProvEntity) for n in used_entities):
            self.used_entities = used_entities
        else:
            raise TypeError('used_entities must be a list of Entity objects')

    def set_generated_entities(self, generated_entities):
        if all(isinstance(n, ProvEntity) for n in generated_entities):
            self.generated_entities = generated_entities
        else:
            raise TypeError('used_entities must be a list of Entity objects')

    def set_wasInformedBy(self, wasInformedBy):
        if type(wasInformedBy) is ProvActivity:
            self.wasInformedBy = wasInformedBy
        else:
            raise TypeError('wasAssociatedWith must be an Activity, not a %s' % type(wasInformedBy))

    def make_graph(self):
        """
        Specialises RdfClass.make_graph()

        :return: an rdflib Graph object
        """
        OwlClass.make_graph(self)

        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        PROV = Namespace('http://www.w3.org/ns/prov#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROV.Activity))

        if self.wasAssociatedWith:
            self.g = self.g + self.wasAssociatedWith.get_graph()
            self.g.add((URIRef(self.uri),
                        PROV.wasAssociatedWith,
                        URIRef(self.wasAssociatedWith.uri)))

        if self.startedAtTime:
            self.g.add((URIRef(self.uri),
                        PROV.startedAtTime,
                        Literal(self.startedAtTime.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))

        if self.endedAtTime:
            self.g.add((URIRef(self.uri),
                        PROV.endedAtTime,
                        Literal(self.endedAtTime.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))

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
            self.g = self.g + self.wasInformedBy.get_graph()
            self.g.add((URIRef(self.uri),
                        PROV.wasInformedBy,
                        URIRef(self.wasInformedBy.uri)))

    def get_graph(self):
        """
        Generates the RDF graph of this class

        :return: This class's RDF graph
        """
        if not self.g:
            self.make_graph()

        return self.g