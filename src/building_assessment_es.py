from experta import *

# Define a fact class to represent building assessment data
class BuildingAssessment(Fact):
    """Fact schema for building assessment."""
    sar_backscatter = Field(bool, default=False)  # Significant SAR backscatter decrease
    cracks = Field(str, default="none")  # e.g., 'none', 'minor', 'moderate', 'severe'
    crack_confidence = Field(float, default=1.0)  # Confidence in crack assessment (0.0 to 1.0)
    load_bearing_cracks = Field(bool, default=False)  # Cracks in load-bearing walls
    crack_width = Field(float, default=0.0)  # Width of cracks in mm
    overcrowding = Field(bool, default=False)  # Is the building overcrowded?
    hazardous_zone = Field(bool, default=False)  # Is the building in a hazardous zone?
    radiation_level = Field(float, default=0.0)  # Radiation level in material or soil
    radiation_confidence = Field(float, default=1.0)  # Confidence in the radiation measurement (0.0 to 1.0)
    unexploded_ordnance = Field(bool, default=False)  # Presence of minefields or unexploded ordnance
    conflicting_data = Field(bool, default=False)  # Conflicting SAR and optical data
    significant_difference = Field(bool, default=False)  # Significant difference in damage assessments
    missing_records = Field(bool, default=False)  # Missing pre- and post-war property records
    critical_infrastructure = Field(bool, default=False)  # Is near critical infrastructure
    hospitals_or_schools = Field(bool, default=False)  # Proximity to hospitals or schools
    population_displacement = Field(bool, default=False)  # Population displacement exceeding housing capacity
    contaminated_materials = Field(bool, default=False)  # Use of contaminated materials
    outdated_design = Field(bool, default=False)  # Building design predates modern codes
    renewable_energy_possible = Field(bool, default=False)  # Feasibility of renewable energy integration
    urban_proximity = Field(bool, default=False)  # Close to urban center
    infrastructure_damaged = Field(bool, default=False)  # Damaged infrastructure near urban center
    radar_stable = Field(bool, default=False)  # Stable radar backscatter over multiple intervals
    cracks_worsening = Field(bool, default=False)  # Minor cracks worsening over time
    damaged_utilities = Field(bool, default=False)  # Damaged sewer or water pipes
    access_to_power = Field(bool, default=False)  # Access to power reduces reconstruction priority
    multiple_properties = Field(bool, default=False)  # Owner has multiple properties
    at_least_one_livable = Field(bool, default=False)  # At least one property is livable
    multiple_families = Field(bool, default=False)  # Building serves multiple families
    income_below_poverty = Field(bool, default=False)  # Income below poverty threshold
    vulnerable_population = Field(bool, default=False)  # Houses vulnerable groups (e.g., elderly, children)
    road_inaccessibility = Field(bool, default=False)  # Roads to the building are inaccessible
    temporary_shelter_needed = Field(bool, default=False)  # Displaced residents require temporary housing

# Define priority mapping for actions
PRIORITY_MAP = {
    "Prohibit rebuilding: Radiation level exceeds safe limits.": 95,
    "Reconstruction Delayed: Located in hazardous zone.": 100,
    "Reconstruction Delayed: Minefields or unexploded ordnance detected.": 90,
    "High Priority: Houses vulnerable populations (e.g., elderly, children).": 85,
    "High Priority: Reconstruction due to overcrowding.": 70,
    "Critical Priority: Near critical infrastructure (e.g., hospitals, schools).": 60,
    "Moderate: Further Inspection Needed.": 55,
    "High Priority: Provide temporary shelter for displaced residents.": 50,
    "Moderate Priority: Repairs suggested for damaged utilities.": 40,
    "Minor Damage: Routine Repairs.": 30,
}

# Define the rule-based system class
class BuildingAssessmentExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.prioritized_actions = []  # Store actions with priorities

    def declare_action(self, action, confidence=1.0):
        # Adjust priority based on confidence
        base_priority = PRIORITY_MAP.get(action, 50)
        adjusted_priority = base_priority * confidence  # Scale priority by confidence level
        self.prioritized_actions.append((adjusted_priority, action))

    def print_prioritized_actions(self):
        # Sort actions by priority and print
        self.prioritized_actions.sort(reverse=True, key=lambda x: x[0])
        for priority, action in self.prioritized_actions:
            print(f"Priority {priority:.1f}: {action}")

    # Structural Damage Assessment Rules
    @Rule(BuildingAssessment(cracks='severe', crack_confidence=MATCH.conf))
    def severe_cracks_with_uncertainty(self, conf):
        if conf >= 0.8:
            self.declare_action("Immediate repairs needed due to severe cracks.", confidence=conf)

    @Rule(BuildingAssessment(sar_backscatter=True))
    def severe_sar_damage(self):
        self.declare_action("Severe Damage: Reconstruction Priority.")

    @Rule(BuildingAssessment(load_bearing_cracks=True, crack_width=0.0))
    def load_bearing_cracks(self):
        self.declare_action("Severe: Immediate Repairs Required.")

    @Rule(BuildingAssessment(cracks="moderate"))
    def moderate_cracks(self):
        self.declare_action("Moderate: Repairs Suggested.")

    @Rule(BuildingAssessment(cracks="minor", load_bearing_cracks=False))
    def minor_surface_cracks(self):
        self.declare_action("Minor Damage: Routine Repairs.")

    @Rule(BuildingAssessment(load_bearing_cracks=True, crack_width=MATCH.width))
    def severe_large_crack(self, width):
        if width > 20.0:
            self.declare_action("Severe: Immediate Repairs Required.")

    @Rule(BuildingAssessment(urban_proximity=True, infrastructure_damaged=True))
    def urban_infrastructure_damage(self):
        self.declare_action("Recommendation: Temporary housing near urban center.")

    @Rule(BuildingAssessment(renewable_energy_possible=True))
    def renewable_energy_integration(self):
        self.declare_action("Recommendation: Integrate renewable energy systems for sustainable rebuilding.")

    @Rule(BuildingAssessment(radiation_level=MATCH.radiation, radiation_confidence=MATCH.conf))
    def high_radiation_with_uncertainty(self, radiation, conf):
        if radiation > 1.0 and conf >= 0.7:
            self.declare_action("Prohibit rebuilding: Radiation level exceeds safe limits.", confidence=conf)

    @Rule(BuildingAssessment(hazardous_zone=True))
    def hazardous_zone_priority(self):
        self.declare_action("Reconstruction Delayed: Located in hazardous zone.")

    @Rule(BuildingAssessment(overcrowding=True))
    def overcrowding_priority(self):
        self.declare_action("High Priority: Reconstruction due to overcrowding.")

    @Rule(BuildingAssessment(vulnerable_population=True))
    def vulnerable_population_priority(self):
        self.declare_action("High Priority: Houses vulnerable populations (e.g., elderly, children).")

    @Rule(BuildingAssessment(temporary_shelter_needed=True))
    def temporary_shelter_priority(self):
        self.declare_action("High Priority: Provide temporary shelter for displaced residents.")

    @Rule(BuildingAssessment(unexploded_ordnance=True))
    def minefields_present(self):
        self.declare_action("Reconstruction Delayed: Minefields or unexploded ordnance detected.")

    @Rule(BuildingAssessment(critical_infrastructure=True))
    def critical_infrastructure_priority(self):
        self.declare_action("Critical Priority: Near critical infrastructure (e.g., hospitals, schools).")

    @Rule(BuildingAssessment(radar_stable=True))
    def stable_radar_backscatter(self):
        self.declare_action("No Damage: Low Priority.")

    @Rule(BuildingAssessment(contaminated_materials=True))
    def contaminated_materials_priority(self):
        self.declare_action("Reconstruction Delayed: Contaminated materials detected, remediation required.")

    @Rule(BuildingAssessment(outdated_design=True))
    def recommend_retrofitting(self):
        self.declare_action("Recommend retrofitting for outdated building design.")

    @Rule(BuildingAssessment(population_displacement=True))
    def population_displacement_priority(self):
        self.declare_action("High Priority: Use pallet or container homes.")

    @Rule(BuildingAssessment(damaged_utilities=True))
    def damaged_utilities_priority(self):
        self.declare_action("Moderate Priority: Repairs suggested for damaged utilities.")

    @Rule(BuildingAssessment(significant_difference=True))
    def significant_differences_priority(self):
        self.declare_action("Moderate: Further Inspection Needed.")

    @Rule(BuildingAssessment(conflicting_data=True))
    def conflicting_data_priority(self):
        self.declare_action("Uncertain: Requires Field Validation.")

    @Rule(BuildingAssessment(missing_records=True))
    def use_geospatial_data(self):
        self.declare_action("Use geospatial data and neighboring properties for estimation.")

    @Rule(BuildingAssessment(hospitals_or_schools=True))
    def prioritize_hospitals_schools(self):
        self.declare_action("Critical Priority: Hospitals or schools zone reconstruction.")

    @Rule(BuildingAssessment(cracks_worsening=True))
    def worsening_cracks_priority(self):
        self.declare_action("Reclassify as Moderate Damage: Cracks worsening over time.")

    @Rule(BuildingAssessment(access_to_power=True))
    def lower_priority_energy(self):
        self.declare_action("Lower Priority: Energy resource allocation not required.")

    @Rule(BuildingAssessment(multiple_properties=True, at_least_one_livable=True))
    def deprioritize_reconstruction(self):
        self.declare_action("Deprioritize: At least one livable property available.")

    @Rule(BuildingAssessment(multiple_families=True))
    def prioritize_multiple_families(self):
        self.declare_action("High Priority: Building serves multiple families.")

    @Rule(BuildingAssessment(income_below_poverty=True))
    def income_priority(self):
        self.declare_action("High Priority: Income below poverty threshold.")

    @Rule(BuildingAssessment(road_inaccessibility=True))
    def road_inaccessibility_priority(self):
        self.declare_action("Reconstruction Delayed: Clear road access before rebuilding.")