# -*- coding: utf-8 -*-

from ckanext.dcat.profiles import RDFProfile
from rdflib.namespace import Namespace, RDF

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
ADMS = Namespace("http://www.w3.org/ns/adms#")
ORG = Namespace("http://www.w3.org/ns/org#")
FRAPO = Namespace("http://purl.org/cerif/frapo/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
SPDX = Namespace('http://spdx.org/rdf/terms#')
SCHEMA = Namespace('http://schema.org/')

namespaces = {
    'dct': DCT,
    'dcat': DCAT,
    'adms': ADMS,
    'org': ORG,
    'frapo': FRAPO,
    'rdfs': RDFS,
    'foaf': FOAF,
    'spdx': SPDX,
    'schema': SCHEMA
}

class CoatDcatProfile(RDFProfile):
    '''
        A custom profile to add COAT fields to the ckanext-dcat RDF serializer.
        Modified from EuropeanDCATAPProfile
    '''

    def graph_from_dataset(self, dataset_dict, dataset_ref):

        g = self.g

        #for prefix, namespace in namespaces.iteritems():
        #    g.bind(prefix, namespace)

        

