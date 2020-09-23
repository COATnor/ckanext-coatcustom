# -*- coding: utf-8 -*-

from ckanext.dcat.profiles import RDFProfile
from rdflib import BNode, Literal, URIRef
from rdflib.namespace import Namespace, RDF

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
ADMS = Namespace("http://www.w3.org/ns/adms#")
ORG = Namespace("http://www.w3.org/ns/org#")
FRAPO = Namespace("http://purl.org/cerif/frapo/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
SPDX = Namespace('http://spdx.org/rdf/terms#')
VCARD = Namespace('https://www.w3.org/TR/vcard-rdf/')
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
    'vcard': VCARD,
    'schema': SCHEMA
}

class CoatDcatProfile(RDFProfile):
    '''
        A custom profile to add COAT fields to the ckanext-dcat RDF serializer.
        Modified from EuropeanDCATAPProfile
    '''

    def graph_from_catalog(self, catalog_dict, catalog_ref):

        g = self.g

        publisher = URIRef("https://coat.no")
        description = "DCAT Catalog for the COAT project: Climate-ecological Observatory for Arctic Tundra"

        agent = URIRef(FOAF.agent)
        g.add((agent, FOAF.agent, publisher))


        # Adding Catalog elements
        g.add((catalog_ref, DCT.publisher, agent))
        g.add((catalog_ref, DCT.description, Literal(description)))


    def graph_from_dataset(self, dataset_dict, dataset_ref):

        g = self.g

        for prefix, namespace in namespaces.iteritems():
            g.bind(prefix, namespace)

        # Here find only the metadata elements which are not already serialized to DCAT
        identifier = self._get_dataset_value(dataset_dict,'identifier')
        doi_identifier = self._get_dataset_value(dataset_dict, 'doi')
        version = self._get_dataset_value(dataset_dict, 'version')
        license_id = self._get_dataset_value(dataset_dict, 'license_id')
        email = self._get_dataset_value(dataset_dict, 'author_email')
        position = self._get_dataset_value(dataset_dict, 'position')
        publisher = self._get_dataset_value(dataset_dict, 'publisher')
        associated_parties = self._get_dataset_value(dataset_dict, 'associated_parties')
        persons = self._get_dataset_value(dataset_dict, 'persons')
        temporal_start = self._get_dataset_value(dataset_dict, 'temporal_Start')
        temporal_end = self._get_dataset_value(dataset_dict, 'temporal_end')
        location = self._get_dataset_value(dataset_dict, 'location')
        scientific_name = self._get_dataset_value(dataset_dict, 'scientific_name')
        resource_citations = self._get_dataset_value(dataset_dict, 'resource_citations')
        scripts = self._get_dataset_value(dataset_dict, 'scripts')
        protocol = self._get_dataset_value(dataset_dict, 'protocol')
        bibliography = self._get_dataset_value(dataset_dict, 'bibliography')
        funding = self._get_dataset_value(dataset_dict, 'funding')
        downloads = self._get_dataset_value(dataset_dict, 'downloads')




        if doi_identifier:
            #doi_ref = URIRef(doi_identifier)
            g.remove((dataset_ref, DCT.identifier, identifier))
            g.add((dataset_ref, DCT.identifier, Literal(doi_identifier)))

        if license_id:
            g.add((dataset_ref, DCT.license, Literal(license_id)))

        if email:
            g.add((dataset_ref, VCARD.hasEmail, Literal(email)))

        ##TODO: FIX problem! Not going to dcat:contactPoint
        if position:
            g.add((DCAT.contactPoint, VCARD.hasRole, Literal(position)))

        if publisher:
            old_publisher = g.value(dataset_ref, DCT.publisher)
            g.remove((dataset_ref, DCT.publisher, old_publisher))
            g.add((dataset_ref, DCT.publisher, Literal(publisher)))

        if persons:
            for person in persons.split(","):
                g.add((dataset_ref, VCARD.coworker, Literal(person)))

        if temporal_start and temporal_end:
            pass








