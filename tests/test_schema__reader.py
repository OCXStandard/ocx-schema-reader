from unittest import TestCase
from pathlib import Path
import yaml
from ocx_schema_reader.utils import ROOT_DIR
from ocx_schema_reader.schema_reader import OcxSchema
import logging
from ocx_xml.xml_parser import LxmlParser

config = Path(ROOT_DIR) / 'ocx_schema_reader' / 'config.yaml'
MODULE_CONFIG = config.absolute()

with open(MODULE_CONFIG) as f:
    app_config = yaml.safe_load(f)

DEFAULT_SCHEMA = app_config.get('DEFAULT_SCHEMA')
SCHEMA_FOLDER = app_config.get('SCHEMA_FOLDER')

logger = logging.getLogger()
schema_reader = OcxSchema(logger, SCHEMA_FOLDER)


class TestOcxSchema(TestCase):
    def test_parse_schema(self):
        result = schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.assertTrue(result)

    def test_schema_version(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        version = schema_reader.get_schema_version()
        self.assertEqual(version, '2.8.7')

    def test_get_schema_folder(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test_get_default_schema(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test_is_parsed(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.assertTrue(schema_reader.is_parsed())

    def test_process_ocx_elements(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test_process_attributes(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test_process_children(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test__process_attribute(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test__process_child(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test__get_element(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test__get_element_from_type(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test__find_parents(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test__find_all_my_parents(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test_get_ocx_element_from_type(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test_get_prefix_from_namespace(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test_add_namespace(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test_get_namespaces(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test_get_all_schema_elements(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        result = schema_reader._get_all_schema_elements()
        self.assertEqual(len(result), 637)

    def test_get_ocx_elements(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        result = schema_reader.get_ocx_elements()
        self.assertEqual(len(result), 637)

    def test_schema_changes(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        # Filter out only '2.8.6' changes
        result = [v for v in schema_reader.get_schema_changes()['Version'] if '2.8.6' in v]
        self.assertEqual(len(result), 29)

    def test_get_schema_elements(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        self.fail()

    def test_get_schema_complex_types(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        result = schema_reader._get_schema_complex_types()
        self.assertListEqual(
            result,
            ['{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ApplicationRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Arrangement_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}BarSection_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}BoundedRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}BoundingBox_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}BracketParameters_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}BracketRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Bracket_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}BuilderInformation_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}BulbFlat_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}BulkCargo_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CellBoundary_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CellConnection_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CellRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Cell_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ChildRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Circle3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CircumArc3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CircumCircle3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ClassCatalogue_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ClassData_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ClassNotation_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ClassParameters_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CompartmentFace_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CompartmentProperties_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Compartment_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ComposedOf_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CompositeCurve3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Cone3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ConnectedBracketRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ConnectionConfiguration_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Contour3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ControlPoint_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ControlPtList_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CoordinateSystem_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CrossFlow_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Curve3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CutBy_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Cylinder3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}CylindricalAxes_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}DescriptionBase_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Description_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}DesignView_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}DocumentBase_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}DoubleBracket_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}EdgeCurveRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}EdgeReinforcement_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Ellipse3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}EndCutRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}EndCut_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}EntityBase_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}EntityRefBase_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Equipment_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ExternalGeometryRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ExtrudedSurface_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}FeatureCope_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}FlangeEdgeReinforcement_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}FlatBar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Form_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}FrameTables_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}FreeEdgeCurve3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}GaseousCargo_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}GeometryRepresentation_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}GridRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}GridSpacingSystem_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}HalfRoundBar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Header_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}HexagonBar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Hole2DContour_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Hole2D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}HoleRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}HoleShapeCatalogue_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}IBar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}IdBase_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Inclination_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}KnotVector_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}LBarOF_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}LBarOW_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}LBar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}LimitedBy_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Line3DList_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Line3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}LiquidCargo_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}LugPlateRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}MaterialCatalogue_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}MaterialRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Material_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Member_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}NURBS3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}NURBSProperties_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}NURBSSurface_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}OccurrenceGroup_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Occurrence_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}OctagonBar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}OcxItemPtr_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}PanelRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Panel_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ParametricCircle_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ParametricHole2D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}PenetratingObject_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Penetration_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}PhysicalProperties_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}PhysicalSpace_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}PillarRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Pillar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Plane3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}PlateMaterial_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}PlateRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Plate_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Point3DList_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Point3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}PolyLine3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}PrincipalParticulars_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ProcessLayer_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ProductView_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Quantity_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}RadialCylinder_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}RectangularHole_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}RectangularMickeyMouseEars_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}RectangularTube_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}RefPlane_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}RefPlanes_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ReferencePlane_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ReferencePlanes_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ReferenceSurfaces_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Reference_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}RootRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}RoundBar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SchemaChange_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SeamRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Seam_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SectionProperties_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SectionRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ShipDesignation_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SingleBracket_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SlotParameters_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Sphere3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SplitBy_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SquareBar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}StatutoryData_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}StiffenedBy_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}StiffenerRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Stiffener_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}StructurePart_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SuperElliptical_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SurfaceCollection_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SurfaceRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Surface_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Sweep_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}SymmetricalHole_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}TBar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}TonnageData_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}TraceLine_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Transformation_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Tube_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}UBar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}UnboundedGeometry_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}UnitCargo_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}UserDefinedBarSection_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}UserDefinedParameter_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Vector3D_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}VesselGrid_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}Vessel_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}WebStiffenerRef_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}WebStiffenerWithDoubleBracket_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}WebStiffenerWithSingleBracket_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}WebStiffener_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}XGrid_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}XSectionCatalogue_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}YGrid_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ZBar_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ZGrid_T',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}ocxXML_T',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}AmountOfSubstanceType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}DimensionSetType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}DimensionType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}ElectricCurrentType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}EnumeratedRootUnitType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}LengthType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}LuminousIntensityType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}MassType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}NameType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}RootUnitsType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}SymbolType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}ThermodynamicTemperatureType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}TimeType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}UnitSetType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}UnitType',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}UnitsMLType']
        )

    def test_get_schema_simple_types(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        result = schema_reader._get_schema_simple_types()
        self.assertListEqual(
            result,
            ['{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}booleanListType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}classificationSociety',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}curveForm_enum',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}doubleListType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}floatListType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}guid',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}integerListType']
        )

    def test_get_schema_attributes(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        result = schema_reader._get_schema_attributes()
        self.assertListEqual(
            result,
            ['{http://www.w3.org/XML/1998/namespace}base', '{http://www.w3.org/XML/1998/namespace}id',
             '{http://www.w3.org/XML/1998/namespace}lang', '{http://www.w3.org/XML/1998/namespace}space',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}GUIDRef',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}additionalNotations',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}application_version',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}asymmetric',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}author',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}author',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}blockCoefficientClass',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}bulkCargoType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}callSign',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}compartmentPurpose',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}count',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}date',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}degree',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}designSpeedAhead',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}designSpeedAstern',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}designer',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}documentation',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}edgeReinforcement',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}element',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}exponent',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}externalRef',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}firstGridNumber',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}flagState',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}form',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}freeboardType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}functionType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}gaseousCargoType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}geometryFormat',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}grade',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}hasBilgeKeel',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}hasDeadweightLessThan',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}hasEdgeReinforcement',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}hull',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}iceClass',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}id',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}identification',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}is2D',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}isClosed',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}isGlobal',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}isMainSystem',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}isMainSystem',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}isRational',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}isReversed',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}isReversed',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}isUVSpace',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}isUVspace',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}language',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}lengthClass',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}lengthSolas',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}license',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}license',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}liquidCargoType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}liquidState',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}localRef',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}locationRef',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}machinery',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}manufacture',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}name',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}name',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}newbuildingSociety',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}newbuildingSocietyName',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}numCtrlPts',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}numCtrlPts',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}numKnots',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}numKnots',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}numberIMO',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}numberOfDecksAbove',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}numberOfParameters',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}numberOfSupports',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}numericvalue',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}organization',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}originating_system',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}owner',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}portRegistration',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}position',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}refType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}scantlingsDraught',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}schemaVersion',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}serviceArea',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}serviceFactor',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}shipName',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}shipType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}shortID',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}slotType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}sniped',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}society',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}societyName',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}symmetricFlange',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}tightness',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}time_stamp',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}typeCode',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}unit',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}unitCargoType',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}value',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}version',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}weight',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}x',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}y',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}yard',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}yearOfBuild',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}z',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}dimensionURL',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}dimensionless',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}initialUnit',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}powerNumerator',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}prefix',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}sourceName',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}sourceURL',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}symbol',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}symbol',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}symbol',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}symbol',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}symbol',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}symbol',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}symbol',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}type',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}unit']
        )

    def test_get_schema_attribute_groups(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        groups = schema_reader._get_schema_attribute_groups()
        self.assertListEqual(
            groups,
            ['{http://www.w3.org/XML/1998/namespace}specialAttrs',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}barSectionAttributes',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}externalRefAttributes',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}header',
             '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}nurbsAttributes',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}dimensionURL',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}initialUnit',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}powerRational',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}prefix',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}sourceName',
             '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}sourceURL']
        )

    def test_summary_table(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        summary = schema_reader.tbl_summary()
        self.assertDictEqual(summary,
            {
                'Item':
                    ['Schema Version', 'Number of element types', 'Number of attribute types',
                     'Number of complexType types', 'Number of simpleType types', 'Number of attributeGroup types',
                     'Number of namespaces', 'xml', 'xs', 'vc', 'xlink', 'ocx', 'unitsml', None, 'xsd'],
                'Value':
                    ['2.8.7', 334, 121, 189, 7, 11, 8, 'http://www.w3.org/XML/1998/namespace',
                     'http://www.w3.org/2001/XMLSchema', 'http://www.w3.org/2007/XMLSchema-versioning',
                     'http://www.w3.org/1999/xlink', 'https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd',
                     'urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18',
                     'urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18',
                     'http://www.w3.org/2001/XMLSchema']
            }
        )

    def test_tbl_attribute_groups(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        groups = schema_reader.tbl_attribute_groups()
        self.assertDictEqual(
            groups,
                 {'Prefix': ['xml', 'ocx', 'ocx', 'ocx', 'ocx', None, None, None, None, None, None],
                  'Name': ['specialAttrs', 'barSectionAttributes', 'externalRefAttributes', 'header',
                           'nurbsAttributes', 'dimensionURL', 'initialUnit', 'powerRational', 'prefix',
                           'sourceName', 'sourceURL'],
                  'Tag': ['{http://www.w3.org/XML/1998/namespace}specialAttrs',
                          '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}barSectionAttributes',
                          '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}externalRefAttributes',
                          '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}header',
                          '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}nurbsAttributes',
                          '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}dimensionURL',
                          '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}initialUnit',
                          '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}powerRational',
                          '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}prefix',
                          '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}sourceName',
                          '{urn:oasis:names:tc:unitsml:schema:xsd:UnitsMLSchema_lite-0.9.18}sourceURL'],
                  'Base': ['schema_versions/xml.xsd', 'schema_versions/OCX_Schema.xsd',
                           'schema_versions/OCX_Schema.xsd', 'schema_versions/OCX_Schema.xsd',
                           'schema_versions/OCX_Schema.xsd', 'schema_versions/unitsmlSchema_lite-0.9.18.xsd',
                           'schema_versions/unitsmlSchema_lite-0.9.18.xsd',
                           'schema_versions/unitsmlSchema_lite-0.9.18.xsd',
                           'schema_versions/unitsmlSchema_lite-0.9.18.xsd',
                           'schema_versions/unitsmlSchema_lite-0.9.18.xsd',
                           'schema_versions/unitsmlSchema_lite-0.9.18.xsd'],
                  'Source line': [157, 7560, 3043, 2327, 5587, 189, 107, 137, 147, 117, 127]})

    def test_tbl_simple_types(self):
        if not schema_reader.is_parsed():
            schema_reader._parse_schema(DEFAULT_SCHEMA)
        result = schema_reader.tbl_simple_types()
        self.assertDictEqual(
            result, {
                'Prefix': ['ocx', 'ocx', 'ocx', 'ocx', 'ocx', 'ocx', 'ocx'],
                'Name': ['booleanListType', 'classificationSociety', 'curveForm_enum', 'doubleListType',
                         'floatListType', 'guid', 'integerListType'],
                'Tag': ['{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}booleanListType',
                        '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}classificationSociety',
                        '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}curveForm_enum',
                        '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}doubleListType',
                        '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}floatListType',
                        '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}guid',
                        '{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}integerListType'],
                'Base': ['schema_versions/OCX_Schema.xsd', 'schema_versions/OCX_Schema.xsd',
                         'schema_versions/OCX_Schema.xsd', 'schema_versions/OCX_Schema.xsd',
                         'schema_versions/OCX_Schema.xsd', 'schema_versions/OCX_Schema.xsd',
                         'schema_versions/OCX_Schema.xsd'],
                'Source line': [7996, 7688, 5628, 8010, 8003, 2551, 7989]})


