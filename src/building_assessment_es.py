from experta import *

# Define a fact class to represent building assessment data
class BuildingAssessment(Fact):
    """Fact schema for building assessment."""
    sar_backscatter = Field(bool, default=False)  # Significant SAR backscatter decrease
    cracks = Field(str, default="none")  # e.g., 'none', 'minor', 'moderate', 'severe'
    load_bearing_cracks = Field(bool, default=False)  # Cracks in load-bearing walls
    crack_width = Field(float, default=0.0)  # Width of cracks in mm
    overcrowding = Field(bool, default=False)  # Is the building overcrowded?
    hazardous_zone = Field(bool, default=False)  # Is the building in a hazardous zone?
    radiation_level = Field(float, default=0.0)  # Radiation level in material or soil
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

# Define the rule-based system class
class BuildingAssessmentExpertSystem(KnowledgeEngine):
    # Structural Damage Assessment Rules
    @Rule(BuildingAssessment(sar_backscatter=True))
    def severe_sar_damage(self):
        self.declare(Fact(action="Severe Damage: Reconstruction Priority."))

    @Rule(BuildingAssessment(load_bearing_cracks=True))
    def load_bearing_cracks(self):
        self.declare(Fact(action="Severe: Immediate Repairs Required."))

    @Rule(BuildingAssessment(cracks='moderate', load_bearing_cracks=False))
    def moderate_damage(self):
        self.declare(Fact(action="Moderate: Repairs Suggested."))

    @Rule(BuildingAssessment(cracks='none', significant_difference=True))
    def computational_instability(self):
        self.declare(Fact(action="Moderate: Further Inspection Needed."))

    @Rule(BuildingAssessment(load_bearing_cracks=True, crack_width=MATCH.width & (lambda width: width > 20)))
    def severe_large_crack(self, width):
        self.declare(Fact(action=f"Severe: Immediate action required for crack width {width} mm."))

    @Rule(BuildingAssessment(cracks='minor', load_bearing_cracks=False))
    def minor_cracks(self):
        self.declare(Fact(action="Minor Damage: Routine Repairs."))

    # Hazard and Environmental Challenges
    @Rule(BuildingAssessment(hazardous_zone=True))
    def hazardous_zone_priority(self):
        self.declare(Fact(action="High Risk: Reconstruction Delayed."))

    @Rule(BuildingAssessment(radiation_level=MATCH.radiation))
    def high_radiation(self, radiation):
        if radiation > 1.0:  # Check the condition explicitly
            self.declare(Fact(action=f"Prohibit rebuilding: Radiation level is {radiation} mSv/year."))

    @Rule(BuildingAssessment(unexploded_ordnance=True))
    def minefields_present(self):
        self.declare(Fact(action="Reconstruction Delayed: Minefields or unexploded ordnance detected."))

    # Data and Inspection Uncertainty
    @Rule(BuildingAssessment(conflicting_data=True))
    def conflicting_data_priority(self):
        self.declare(Fact(action="Uncertain: Requires Field Validation."))

    @Rule(BuildingAssessment(significant_difference=True))
    def expert_review_priority(self):
        self.declare(Fact(action="Uncertain: Flag for expert review."))

    @Rule(BuildingAssessment(missing_records=True))
    def use_geospatial_data(self):
        self.declare(Fact(action="Use geospatial data and neighboring properties for estimation."))

    # Reconstruction and Resource Allocation
    @Rule(BuildingAssessment(critical_infrastructure=True))
    def critical_infrastructure_priority(self):
        self.declare(Fact(action="Critical Priority: Near critical infrastructure (e.g., hospitals, schools)."))

    @Rule(BuildingAssessment(hospitals_or_schools=True))
    def prioritize_hospitals_schools(self):
        self.declare(Fact(action="Critical Priority: Hospitals or schools zone reconstruction."))

    @Rule(BuildingAssessment(population_displacement=True))
    def population_displacement_priority(self):
        self.declare(Fact(action="High Priority: Use pallet or container homes."))

    @Rule(BuildingAssessment(overcrowding=True))
    def overcrowding_priority(self):
        self.declare(Fact(action="High Priority: Reconstruction due to overcrowding."))

    # Sustainability and Material Considerations
    @Rule(BuildingAssessment(contaminated_materials=True))
    def contaminated_materials_priority(self):
        self.declare(Fact(action="Reconstruction Delayed: Contaminated materials detected, remediation required."))

    @Rule(BuildingAssessment(outdated_design=True))
    def recommend_retrofitting(self):
        self.declare(Fact(action="Recommend retrofitting for outdated building design."))

    @Rule(BuildingAssessment(renewable_energy_possible=True))
    def renewable_energy_integration(self):
        self.declare(Fact(action="Recommendation: Integrate renewable energy systems for sustainable rebuilding."))

    # Temporary and Emergency Housing
    @Rule(BuildingAssessment(temporary_shelter_needed=True))
    def temporary_shelter_priority(self):
        self.declare(Fact(action="High Priority: Provide temporary shelter for displaced residents."))

    @Rule(BuildingAssessment(urban_proximity=True, infrastructure_damaged=True))
    def recommend_temporary_housing(self):
        self.declare(Fact(action="Recommendation: Temporary housing near urban center."))

    # Monitoring and Maintenance
    @Rule(BuildingAssessment(radar_stable=True))
    def no_damage_low_priority(self):
        self.declare(Fact(action="No Damage: Low Priority."))

    @Rule(BuildingAssessment(cracks_worsening=True))
    def worsening_cracks(self):
        self.declare(Fact(action="Reclassify as Moderate Damage: Cracks worsening over time."))

    # Utility and Community Rules
    @Rule(BuildingAssessment(damaged_utilities=True))
    def damaged_utilities_priority(self):
        self.declare(Fact(action="Moderate Priority: Repairs suggested for damaged utilities."))

    @Rule(BuildingAssessment(access_to_power=True))
    def lower_priority_energy(self):
        self.declare(Fact(action="Lower Priority: Energy resource allocation not required."))

    @Rule(BuildingAssessment(multiple_properties=True, at_least_one_livable=True))
    def deprioritize_reconstruction(self):
        self.declare(Fact(action="Deprioritize: At least one livable property available."))

    @Rule(BuildingAssessment(multiple_families=True))
    def prioritize_multiple_families(self):
        self.declare(Fact(action="High Priority: Building serves multiple families."))

    @Rule(BuildingAssessment(income_below_poverty=True))
    def income_priority(self):
        self.declare(Fact(action="High Priority: Income below poverty threshold."))

    @Rule(BuildingAssessment(vulnerable_population=True))
    def vulnerable_population_priority(self):
        self.declare(Fact(action="High Priority: Houses vulnerable populations (e.g., elderly, children)."))

    @Rule(BuildingAssessment(road_inaccessibility=True))
    def road_inaccessibility_priority(self):
        self.declare(Fact(action="Reconstruction Delayed: Clear road access before rebuilding."))