#  Copyright (c) 2022 OCX Consortium (https://3docx.org). See the LICENSE.

from collections import defaultdict
from logging import Logger
import re

from lxml.etree import Element, QName, ElementTextIterator

from ocx_xml.xml_element import LxmlElement


class SchemaHelper:
    """ A utility class for retrieving OCX attributes and information from an OCX xsd element """
    @classmethod
    def is_reference(cls, element:Element) -> bool:
        """ Check if the xsd element references a global element
        Returns:
            True if the element has a reference, False otherwise

        """
        return cls.get_reference(element) is not 'None'

    @classmethod
    def get_reference(cls, element:Element) -> str:
        """ The referenced element
        Returns:
            The reference (unique tag) to a global element as a str on the form prefix:name.
            Returns None if the element is not a reference.

        """
        attributes = LxmlElement.get_xml_attrib(element)
        ref = attributes.get('ref')
        if ref is None:
            ref = 'None'
        return ref

    @staticmethod
    def get_type(element:Element) -> str:
        """ The element type given by the element attribute or by its complexContent
        Returns:
            The type of the global element as a str on the form prefix:name
            If the element has no type, 'untyped' is returned.

        """
        schema_type = None
        attributes = LxmlElement.get_xml_attrib(element)
        if "type" in attributes:
            schema_type = attributes["type"]
        if "base" in attributes:
            schema_type = attributes["base"]
        if 'ref' in attributes:
            schema_type = attributes['ref']
        # The element may have complexContent
        if len(LxmlElement.find_all_children_with_name(element, 'complexContent')) > 0:
            # complexContent has either an extension or a restriction
            # extension
            base = LxmlElement.find_all_children_with_name_and_attribute(element,'extension', 'base')
            if len(base) > 0:
                schema_type = base[0].get("base")
           # restriction
            base = LxmlElement.find_all_children_with_name_and_attribute(element,'restriction', 'base')
            if len(base) > 0:
                schema_type = base[0].get("base")
        # the element may be a simpleType
        simple_type = LxmlElement.find_all_children_with_name(element, 'simpleType')
        if len(simple_type) > 0:
            # simpleType may have either an extension or a restriction
            # extension
            base = LxmlElement.find_all_children_with_name_and_attribute(simple_type[0], 'extension', 'base')
            if len(base) > 0:
                schema_type = base[0].get("base")
            # restriction
            base = LxmlElement.find_all_children_with_name_and_attribute(simple_type[0], 'restriction', 'base')
            if len(base) > 0:
                schema_type = base[0].get("base")

        # if schemaType is not None:
        #     # Add any missing prefix
        #     if ns_prefix(schemaType) is None:
        #         base = element.base
        #         if base in self.schema.schemaBase:
        #             prefix = self.schema.schemaBase[base]
        #             schemaType = prefix + ":" + schemaType
        # else:
        #     schemaType = "untyped"
        return schema_type

    @staticmethod
    def unique_tag(name: str, namespace: str) -> str:
        """ A unique global tag from the element name and namespace

        Args:
            name: The name of the element
            namespace: The namespace
        Returns:
            global element tag as a str on the form '{namespace}name'

        """

        tag = '{' + namespace + '}' + name
        return tag

    @staticmethod
    def get_schema_version(root: Element) -> str:
        """ Get the current OCX schema version

        Args:
            root: The root element of the schema
        Returns:
            The version string of the OCX schema

        """
        version = 'Missing'
        # root.findall('.//{*}attribute[@name="schemaVersion"]'
        element = LxmlElement.find_all_children_with_attribute_value(root, 'attribute', 'name', 'schemaVersion')
        if len(element) > 0:
            version = element[0].get('fixed')
        return version


    @staticmethod
    def get_schema_changes(root: Element) -> dict:
        schema_changes = defaultdict(list)
        changes = LxmlElement.find_all_children_with_name(root, 'SchemaChange')
        for change in changes:
            schema_changes['Version'].append(change.get("version"))
            schema_changes["Author"].append(change.get("author"))
            schema_changes["Date"].append(change.get("date"))
            # Retrieve the reason for change from the Description element
            description = LxmlElement.find_all_children_with_name(change, 'Description')
            # Parse the text between start and end tag
            if len(description) > 0:
                description = ""
                for text in ElementTextIterator(change[0], with_tail=False):
                    description = description + text
                    text = re.sub("[\n\t\r]", "", description)
                schema_changes["Description"].append(text)
        return schema_changes


class SchemaCardinality:
    """ Class establishing the cardinality of an OCX element """

    def __init__(self, element: Element):
        self.element = element  # Always the local element
        self.cardinality = LxmlElement
        self.lower = ""
        self.upper = ""
        self.default = ""
        self.fixed = ""
        self.choice = False
        self.cardinality(element)

    def cardinality(self, element):
        """ Establish the cardinality of the Element

        Args:
            element: the etree.Element instance

        """
        qn = QName(element)
        attributes = element.attrib
        if qn.localname == "element":
            if "minOccurs" in attributes:
                self.lower = attributes["minOccurs"]
                if self.lower == "0":
                    self.use = "opt."
                else:
                    self.use = "req."
                    if "minOccurs" in attributes:
                        self.lower = attributes["minOccurs"]
                    else:
                        self.lower = "1"
            else:
                self.use = "req."
                self.lower = "1"
            if "maxOccurs" in attributes:
                self.upper = attributes["maxOccurs"]
            else:
                self.upper = "1"
            # Find the closest sequence or choice ancestor which overrules mandatory use
            for item in self.element.iterancestors("{*}sequence", "{*}choice"):
                attributes = item.attrib
                qn = QName(item)
                if qn.localname == "choice":
                    self.choice = True
                if "minOccurs" in attributes:
                    if attributes["minOccurs"] == "0":
                        self.use = "opt."
                        self.lower = "0"
                if "maxOccurs" in attributes:
                    self.upper = attributes["maxOccurs"]
                break
        if qn.localname == "attribute":
            self.upper = "1"
            attributes = self.element.attrib
            if "use" in attributes:
                if attributes["use"] == "required":
                    self.use = "req."
                    self.lower = "1"
            else:
                self.use = "opt."
                self.lower = "0"
            if "default" in attributes:
                self.default = attributes["default"]
            if "fixed" in attributes:
                self.fixed = attributes["fixed"]
        return

    def get_cardinality(self) -> str:
        """ The cardinality of the Element

        Returns:
            The cardinality of the element as a str on the form [lower,upper]

        """
        if self.upper == "unbounded":
            self.upper = "\u221E"  # UTF-8 Infinity symbol
        return "[" + self.lower + "," + self.upper + "]"

    def is_mandatory(self) -> bool:
        if self.use == "req.":
            return True
        else:
            return False

    def is_choice(self) -> bool:
        """ If the Element is a choice or not

        Returns:
            True if the Element is a xs:choice, False otherwise

        """
        return self.choice

    def put_choice(self, choice: bool):
        """ Define wheter the element is a choice or not

        Args:
            choice: True if the element is an xs:choice, False otherwise

        """

        self.choice = choice


class SchemaAttribute:
    def __init__(self, element: Element, tag: str, logger: Logger):
        self.schema = None
        self.log = logger
        self.element = element
        self.tag = tag
        self.namespace = element.nsmap
        #        object = SchemaType(element, schema)
        self.type = object.get_type()
        self.name = object.get_name()
        self.referencedElement = object.get_referenced_element()
        # The element cardinality
        self.cardinalityObject = Cardinality(element, self.referencedElement)
        # The element documentation
        # annotation_object = Annotation(
        #     self.get_name(), self.element, self.referencedElement, logger
        # )
        self.annotation = annotation_object.find_annotation(self.referencedElement)


    def put_annotation(self, text: str):
        """ Override the element documentation using any locally declared annotation
        Args:
            text: The annotation string
        """
        self.annotation = text


    def get_cardinality_object(self) -> SchemaCardinality:
        return self.cardinalityObject

        # Used to override the cardinality


    def put_cardinality(self, cardinality: SchemaCardinality):
        self.cardinalityObject = cardinality


    def get_annotation(self) -> str:
        """ Get the element annotation string
         Returns:
             The annotation string
         """

        return self.annotation


    def get_type(self) -> str:
        return self.type


    def get_name(self) -> str:
        return self.name


    def is_mandatory(self) -> bool:
        if (
                self.get_typed_name() in self.schema.mandatoryElements
        ):  # Force mandatory elements
            return True
        else:
            return self.cardinalityObject.is_mandatory()


    def is_choice(self) -> bool:
        return self.cardinalityObject.is_choice()


    def put_choice(self, choice: bool):
        self.cardinalityObject.put_choice(choice)


    def get_cardinality(self) -> str:
        return self.cardinalityObject.get_cardinality()


    def get_use(self) -> str:
        return self.cardinalityObject.use


    def get_prefix(self) -> str:
        return ns_prefix(self.get_type())


    def get_nsmap(self) -> dict:
        return self.namespace


    def get_typed_name(self) -> str:
        prefix = self.get_prefix()
        name = self.get_name()
        if prefix is not None:
            return prefix + ":" + name
        else:
            return name


    def get_tag(self) -> str:
        if self.tag == "None":
            prefix = self.get_prefix()
            nsmap = self.get_nsmap()
            if prefix in nsmap:
                tag = nsmap[prefix]
            else:
                tag = "*"
            return "{" + tag + "}" + self.get_name()
        else:
            return self.tag


    def is_abstract(self) -> bool:
        if "abstract" in self.element.attrib:
            return True
        else:
            return False

        def get_default(self):
            return self.cardinalityObject.default

        def get_fixed(self):
            return self.cardinalityObject.fixed
