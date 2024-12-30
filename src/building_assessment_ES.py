from experta import *

# Define a fact class to represent building assessment data
class BuildingAssessment(Fact):
    """Fact schema for building assessment."""

    # Structural Factors
    sar_backscatter = Field(bool, default=False)  # Significant SAR backscatter decrease
    cracks = Field(str, default="none")  # Cracks: 'none', 'minor', 'moderate', 'severe'
    crack_confidence = Field(float, default=1.0)  # Confidence in crack assessment (0.0 to 1.0)
    load_bearing_cracks = Field(bool, default=False)  # Cracks in load-bearing walls
    crack_width = Field(float, default=0.0)  # Width of cracks in mm
    cracks_worsening = Field(bool, default=False)  # Minor cracks worsening over time
    radar_stable = Field(bool, default=False)  # Stable radar backscatter over multiple intervals

    # Environmental Factors
    hazardous_zone = Field(bool, default=False)  # Is the building in a hazardous zone?
    hazardous_confidence = Field(float, default=1.0)  # Confidence in hazardous zone assessment (0.0 to 1.0)
    radiation_level = Field(float, default=0.0)  # Radiation level in material or soil
    radiation_confidence = Field(float, default=1.0)  # Confidence in radiation measurement (0.0 to 1.0)
    unexploded_ordnance = Field(bool, default=False)  # Presence of minefields or unexploded ordnance
    ordnance_confidence = Field(float, default=1.0)  # Confidence in unexploded ordnance detection (0.0 to 1.0)
    urban_proximity = Field(bool, default=False)  # Close to urban center
    road_inaccessibility = Field(bool, default=False)  # Roads to the building are inaccessible
    infrastructure_damaged = Field(bool, default=False)  # Damaged infrastructure near urban center
    slope_gradient = Field(float, default=0.0)  # Slope gradient in degrees
    flood_zone_proximity = Field(float, default=0.0)  # Distance to nearest flood zone in meters
    seismic_risk = Field(float, default=0.0)  # Peak Ground Acceleration (PGA) in g

    # Social Factors
    overcrowding = Field(bool, default=False)  # Is the building overcrowded?
    overcrowding_confidence = Field(float, default=1.0)  # Confidence in overcrowding assessment (0.0 to 1.0)
    vulnerable_population = Field(bool, default=False)  # Houses vulnerable groups (e.g., elderly, children)
    vulnerable_confidence = Field(float, default=1.0)  # Confidence in vulnerable population assessment (0.0 to 1.0)
    multiple_families = Field(bool, default=False)  # Building serves multiple families
    income_below_poverty = Field(bool, default=False)  # Owner's income is below the poverty threshold
    population_displacement = Field(bool, default=False)  # Population displacement exceeding housing capacity
    temporary_shelter_needed = Field(bool, default=False)  # Displaced residents require temporary housing

    # Utility and Infrastructure
    damaged_utilities = Field(bool, default=False)  # Damaged sewer or water pipes
    utilities_confidence = Field(float, default=1.0)  # Confidence in damaged utilities assessment (0.0 to 1.0)
    access_to_power = Field(bool, default=False)  # Access to power reduces reconstruction priority
    critical_infrastructure = Field(bool, default=False)  # Is near critical infrastructure
    hospitals_or_schools = Field(bool, default=False)  # Proximity to hospitals or schools
    power_outage_duration = Field(int, default=0)  # Duration of power outage in months
    water_contamination = Field(bool, default=False)  # Indicates bacterial or chemical contamination
    water_access_disrupted = Field(bool, default=False)  # Indicates temporary disruption to water access

    # Design and Data Availability
    outdated_design = Field(bool, default=False)  # Building design predates modern codes
    conflicting_data = Field(bool, default=False)  # Conflicting SAR and optical data
    significant_difference = Field(bool, default=False)  # Significant difference in damage assessments
    missing_records = Field(bool, default=False)  # Missing pre- and post-war property records
    multiple_properties = Field(bool, default=False)  # Owner has multiple properties
    at_least_one_livable = Field(bool, default=False)  # At least one property is livable
    contaminated_materials = Field(bool, default=False)  # Indicates whether materials are contaminated
    renewable_energy_possible = Field(bool, default=False)  # Indicates feasibility of renewable energy integration

# Define priority mapping for actions
PRIORITY_MAP = {
    # Critical and Severe Actions
    "Critical: Reconstruction Delayed due to hazardous zone.": 100,
    "Critical: Reconstruction Delayed due to minefields.": 90,
    "Critical: Reconstruction Delayed due to Landslide Risk.": 100,
    "Critical: Earthquake Reinforcement Required.": 100,
    "Critical Priority: Hospitals or schools zone reconstruction.": 70,
    "Prohibit rebuilding due to high radiation.": 95,
    "Severe: Immediate Repairs Required (SAR Detected).": 85,
    "Severe: Immediate Repairs Required (Visual Assessment).": 85,
    "Severe: Immediate Repairs Required.": 85,
    "Critical: Combined impact of hazardous zone and overcrowding.": 90,
    "Critical: Combined Flood and Water Contamination Risk.": 100,
    "Critical: Landslide Risk Near Critical Infrastructure.": 100,

    # High-Priority Actions
    "High Priority: Vulnerable population safety.": 80,
    "High Priority: Reconstruction due to overcrowding.": 75,
    "High Priority: Temporary housing near urban center for displaced residents.": 75,
    "High Priority: Deploy Temporary Power Sources for Critical Facilities.": 90,
    "High Priority: Use pallet or container homes.": 70,
    "High Priority: Income below poverty threshold.": 70,
    "High Priority: Building serves multiple families.": 70,
    "High Priority: Combined impact of overcrowding and vulnerable population.": 85,
    "High Priority: Restore Utilities for Vulnerable Population.": 80,

    # Moderate Actions
    "Moderate: Flood Zone and Water Contamination Mitigation Required.": 70,
    "Moderate: Repairs suggested for damaged utilities.": 50,
    "Moderate: Incorporate Earthquake-Resistant Design.": 50,
    "Moderate: Proceed with caution due to Landslide Susceptibility.": 50,
    "Moderate: Flood Protection Measures Required.": 50,
    "Moderate Priority: Monitor Power Restoration Timelines.": 50,
    "Moderate Priority: Restore Water Supply Access.": 70,
    "Moderate: Monitor Landslide Risk Near Critical Infrastructure.": 70,

    # Recommendations and Low-Priority Actions
    "Recommendation: Retrofit building to modern design standards.": 50,
    "Recommendation: Import Certified Materials to Ensure Safety.": 50,
    "Recommendation: Mandatory Renewable Energy Integration for Sustainability.": 50,
    "Recommendation: Temporary housing near urban center.": 50,
    "Minor: Routine Repairs Recommended.": 30,
    "Low Priority: Landslide risk is minimal.": 30,
    "Low Priority: Flood risk is minimal.": 30,
    "Low Priority: Seismic risk is minimal.": 30,
    "Low Priority: No immediate repairs required (Radar stable).": 20,
    "Lower Priority: At least one livable property available.": 20,
}

class BuildingAssessmentExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.prioritized_actions = []

    def declare_action(self, action, confidence=1.0):
        """
        Declares an action with a scaled priority based on confidence.
        - If confidence is 1.0, the full priority is used.
        - Lower confidence scales down the priority proportionally.
        """
        base_priority = PRIORITY_MAP.get(action, 50)  # Default to 50 if action not found
        adjusted_priority = base_priority * confidence
        self.prioritized_actions.append((adjusted_priority, action))

    def reset_actions(self):
        """Clears the list of prioritized actions."""
        self.prioritized_actions = []

    def print_prioritized_actions(self, top_n=5, verbose=False):
        """
        Prints the top `n` prioritized actions.
        - If `verbose=True`, includes detailed explanations.
        - If no actions are available, prints a friendly message.
        """
        if not self.prioritized_actions:
            print("No prioritized actions to display.")
            return

        self.prioritized_actions.sort(reverse=True, key=lambda x: x[0])  # Sort by priority (desc)
        for priority, action in self.prioritized_actions[:top_n]:
            if verbose:
                print(f"[Priority: {priority:.1f}] Action: {action}")
            else:
                print(f"Priority {priority:.1f}: {action}")

    def get_top_actions(self, top_n=5):
        """
        Returns the top `n` prioritized actions as a list of tuples.
        Each tuple contains (priority, action).
        """
        self.prioritized_actions.sort(reverse=True, key=lambda x: x[0])
        return self.prioritized_actions[:top_n]

    # Structural Damage Assessment Rules
    @Rule(BuildingAssessment(sar_backscatter=True))
    def severe_sar_damage(self):
        self.declare_action("Severe: Immediate Repairs Required (SAR Detected).")

    @Rule(BuildingAssessment(cracks='severe', crack_confidence=MATCH.conf))
    def severe_cracks_with_uncertainty(self, conf):
        # Treat as normal rule if no confidence is provided
        if conf is None or not (0.0 <= conf <= 1.0): # Ensure confidence is valid
            conf = 1.0
        if conf >= 0.8:
            self.declare_action("Severe: Immediate Repairs Required (Visual Assessment).", confidence=conf)

    @Rule(BuildingAssessment(load_bearing_cracks=True, crack_width=0.0))
    def load_bearing_cracks_rule(self):
        self.declare_action("Severe: Immediate Repairs Required.")

    @Rule(BuildingAssessment(cracks="moderate"))
    def moderate_cracks_rule(self):
        self.declare_action("Moderate: Repairs Suggested.")

    @Rule(BuildingAssessment(cracks="minor", load_bearing_cracks=False, crack_confidence=MATCH.conf))
    def minor_surface_cracks_with_confidence(self, conf):
        if conf is None or not (0.0 <= conf <= 1.0):
            conf = 1.0
        if conf >= 0.5:
            self.declare_action("Minor: Routine Repairs Recommended.", confidence=conf)

    @Rule(BuildingAssessment(load_bearing_cracks=True, crack_width=MATCH.width))
    def severe_large_crack_rule(self, width):
        if width > 20.0:
            self.declare_action("Severe: Immediate Repairs Required.")

    @Rule(BuildingAssessment(cracks_worsening=True))
    def worsening_cracks_priority(self):
        self.declare_action("Reclassify as Moderate Damage: Cracks worsening over time.")

    # Environmental Hazard Rules
    @Rule(BuildingAssessment(hazardous_zone=True, hazardous_confidence=MATCH.conf))
    def hazardous_zone_with_uncertainty(self, conf):
        if conf is None or not (0.0 <= conf <= 1.0): # Ensure confidence is valid
            conf = 1.0
        if conf >= 0.6:
            self.declare_action("Critical: Reconstruction Delayed due to hazardous zone.", confidence=conf)

    @Rule(BuildingAssessment(radiation_level=MATCH.radiation, radiation_confidence=MATCH.conf))
    def high_radiation_with_uncertainty(self, radiation, conf):
        # Default confidence to 1.0 if not provided
        if conf is None or not (0.0 <= conf <= 1.0): # Ensure confidence is valid
            conf = 1.0
        if radiation > 1.0 and conf >= 0.7:
            self.declare_action("Prohibit rebuilding due to high radiation.", confidence=conf)

    @Rule(BuildingAssessment(unexploded_ordnance=True, ordnance_confidence=MATCH.conf))
    def minefields_with_uncertainty(self, conf):
        if conf is None or not (0.0 <= conf <= 1.0): # Ensure confidence is valid
            conf = 1.0
        if conf >= 0.75:
            self.declare_action("Critical: Reconstruction Delayed due to minefields.", confidence=conf)

    @Rule(AND(
    BuildingAssessment(radiation_level=MATCH.radiation, radiation_confidence=MATCH.radiation_conf),
    BuildingAssessment(unexploded_ordnance=True, ordnance_confidence=MATCH.ordnance_conf)
    ))
    def radiation_and_minefields(self, radiation, radiation_conf, ordnance_conf):
        combined_conf = min(radiation_conf, ordnance_conf)
        if radiation > 1.0 and combined_conf >= 0.75:
            self.declare_action("Prohibit rebuilding due to radiation and minefields.", confidence=combined_conf)

    @Rule(BuildingAssessment(contaminated_materials=True))
    def contaminated_materials_priority(self):
        self.declare_action("Critical: Reconstruction Delayed: Contaminated materials detected, remediation required.")
    
    @Rule(
    AND(
        BuildingAssessment(hazardous_zone=True, hazardous_confidence=MATCH.conf),
        BuildingAssessment(slope_gradient=MATCH.slope)  # Use the new slope field
    ))
    def landslide_prone_area_rule(self, conf, slope):
        # Validate inputs
        if conf is None or not (0.0 <= conf <= 1.0):
            conf = 1.0

        # Landslide risk thresholds
        if slope > 30 and conf >= 0.6:  # High risk: Slope > 30° and confidence >= 0.6
            self.declare_action("Critical: Reconstruction Delayed due to Landslide Risk.", confidence=conf)
        elif 20 < slope <= 30 and conf >= 0.5:  # Moderate risk: Slope 20°-30°
            self.declare_action("Moderate: Proceed with caution due to Landslide Susceptibility.", confidence=conf)
        else:  # Low risk: Slope ≤ 20°
            self.declare_action("Low Priority: Landslide risk is minimal.", confidence=conf)

    @Rule(
    BuildingAssessment(flood_zone_proximity=MATCH.distance)
    )
    def flood_zone_rule(self, distance):
        if distance <= 100:  # High risk: Within 100 meters
            self.declare_action("Critical: Reconstruction Delayed due to High Flood Risk.")
        elif 100 < distance <= 500:  # Moderate risk: 100-500 meters
            self.declare_action("Moderate: Flood Protection Measures Required.")
        else:  # Low risk: Beyond 500 meters
            self.declare_action("Low Priority: Flood risk is minimal.")

    @Rule(
    BuildingAssessment(seismic_risk=MATCH.pga)
    )
    def seismic_activity_rule(self, pga):
        if pga > 0.4:  # High risk: Severe shaking likely
            self.declare_action("Critical: Earthquake Reinforcement Required.")
        elif 0.2 < pga <= 0.4:  # Moderate risk: Moderate shaking likely
            self.declare_action("Moderate: Incorporate Earthquake-Resistant Design.")
        else:  # Low risk: Minimal shaking expected
            self.declare_action("Low Priority: Seismic risk is minimal.")

    @Rule(
    AND(
        BuildingAssessment(hazardous_zone=True, hazardous_confidence=MATCH.hazardous_conf),
        BuildingAssessment(overcrowding=True, overcrowding_confidence=MATCH.overcrowding_conf)
    ))
    def hazardous_zone_and_overcrowding_rule(self, hazardous_conf, overcrowding_conf):
        combined_conf = min(hazardous_conf, overcrowding_conf)  # Use the lower confidence level
        if combined_conf >= 0.7:
            self.declare_action("Critical: Combined impact of hazardous zone and overcrowding.", confidence=combined_conf)
    
    @Rule(
    AND(
        BuildingAssessment(flood_zone_proximity=MATCH.distance),
        BuildingAssessment(water_contamination=True)
    ))
    def flood_zone_and_water_contamination_rule(self, distance):
        if distance <= 100:  # High flood risk
            self.declare_action("Critical: Combined Flood and Water Contamination Risk.")
        elif distance <= 500:  # Moderate flood risk
            self.declare_action("Moderate: Flood Zone and Water Contamination Mitigation Required.")

    @Rule(
    AND(
        BuildingAssessment(slope_gradient=MATCH.slope, hazardous_confidence=MATCH.hazardous_conf),
        BuildingAssessment(critical_infrastructure=True)
    ))
    def landslide_risk_and_critical_infrastructure_rule(self, slope, hazardous_conf):
        if slope > 30 and hazardous_conf >= 0.6:  # High landslide risk and hazardous confidence
            self.declare_action("Critical: Landslide Risk Near Critical Infrastructure.", confidence=hazardous_conf)
        elif 20 < slope <= 30 and hazardous_conf >= 0.5:  # Moderate landslide risk
            self.declare_action("Moderate: Monitor Landslide Risk Near Critical Infrastructure.", confidence=hazardous_conf)




    # Data and Assessment Rules
    @Rule(BuildingAssessment(significant_difference=True))
    def significant_differences_priority(self):
        self.declare_action("Moderate: Further Inspection Needed.")

    @Rule(BuildingAssessment(conflicting_data=True))
    def conflicting_data_priority(self):
        self.declare_action("Uncertain: Requires Field Validation.")

    @Rule(BuildingAssessment(missing_records=True))
    def use_geospatial_data(self):
        self.declare_action("Use geospatial data and neighboring properties for estimation.")
    
    @Rule(BuildingAssessment(radar_stable=True))
    def stable_radar_rule(self):
        self.declare_action("Low Priority: No immediate repairs required (Radar stable).")

    @Rule(BuildingAssessment(contaminated_materials=True))
    def certified_materials_rule(self):
        self.declare_action("Recommendation: Import Certified Materials to Ensure Safety.")


    # Social Factors Rules
    @Rule(BuildingAssessment(overcrowding=True, overcrowding_confidence=MATCH.conf))
    def overcrowding_with_uncertainty(self, conf):
        if conf is None or not (0.0 <= conf <= 1.0): # Ensure confidence is valid
            conf = 1.0
        if conf >= 0.7:
            self.declare_action("High Priority: Reconstruction due to overcrowding.", confidence=conf)

    @Rule(BuildingAssessment(vulnerable_population=True, vulnerable_confidence=MATCH.conf))
    def vulnerable_population_with_uncertainty(self, conf):
        if conf is None or not (0.0 <= conf <= 1.0): # Ensure confidence is valid
            conf = 1.0
        if conf >= 0.8:
            self.declare_action("High Priority: Vulnerable population safety.", confidence=conf)

    @Rule(BuildingAssessment(population_displacement=True))
    def population_displacement_priority(self):
        self.declare_action("High Priority: Use pallet or container homes.")

    @Rule(BuildingAssessment(income_below_poverty=True))
    def income_priority(self):
        self.declare_action("High Priority: Income below poverty threshold.")

    @Rule(BuildingAssessment(multiple_families=True))
    def prioritize_multiple_families(self):
        self.declare_action("High Priority: Building serves multiple families.")

    @Rule(BuildingAssessment(multiple_properties=True, at_least_one_livable=True))
    def deprioritize_livable_properties(self):
        self.declare_action("Lower Priority: At least one livable property available.")

    @Rule(
    AND(
        BuildingAssessment(vulnerable_population=True, vulnerable_confidence=MATCH.vulnerable_conf),
        BuildingAssessment(damaged_utilities=True, utilities_confidence=MATCH.utilities_conf)
    ))
    def vulnerable_population_and_damaged_utilities_rule(self, vulnerable_conf, utilities_conf):
        combined_conf = min(vulnerable_conf, utilities_conf)  # Use the lower confidence level
        if combined_conf >= 0.8:  # High confidence threshold
            self.declare_action("High Priority: Restore Utilities for Vulnerable Population.", confidence=combined_conf)

    # Design and Sustainability Rules
    @Rule(BuildingAssessment(outdated_design=True))
    def recommend_retrofitting(self):
        self.declare_action("Recommendation: Retrofit building to modern design standards.")

    @Rule(BuildingAssessment(renewable_energy_possible=True))
    def renewable_energy_integration(self):
        self.declare_action("Recommendation: Integrate renewable energy systems.")

    @Rule(AND(
        BuildingAssessment(urban_proximity=True),
        BuildingAssessment(temporary_shelter_needed=True)
    ))
    def urban_temporary_shelter(self):
        self.declare_action("High Priority: Temporary housing near urban center for displaced residents.")

    @Rule(BuildingAssessment(renewable_energy_possible=True))
    def renewable_energy_rule(self):
        self.declare_action("Recommendation: Mandatory Renewable Energy Integration for Sustainability.")

 
    # Utility and Infrastructure Rules
    @Rule(BuildingAssessment(critical_infrastructure=True))
    def critical_infrastructure_priority(self):
        self.declare_action("Critical: Near critical infrastructure (e.g., hospitals, schools).")

    @Rule(BuildingAssessment(hospitals_or_schools=True))
    def prioritize_hospitals_schools(self):
        self.declare_action("Critical Priority: Hospitals or schools zone reconstruction.")

    @Rule(BuildingAssessment(damaged_utilities=True, utilities_confidence=MATCH.conf))
    def damaged_utilities_with_uncertainty(self, conf):
        if conf is None or not (0.0 <= conf <= 1.0):
            conf = 1.0
        if conf >= 0.8:
            self.declare_action("Moderate: Repairs suggested for damaged utilities.", confidence=conf)

    @Rule(BuildingAssessment(access_to_power=True))
    def lower_priority_energy(self):
        self.declare_action("Lower Priority: Energy resource allocation not required.")

    @Rule(BuildingAssessment(road_inaccessibility=True))
    def road_inaccessibility_priority(self):
        self.declare_action("Reconstruction Delayed: Clear road access before rebuilding.")

    @Rule(
    AND(
        BuildingAssessment(power_outage_duration=MATCH.duration),
        BuildingAssessment(critical_infrastructure=True)
    ))
    def temporary_power_rule(self, duration):
        if duration > 6:  # High priority for outages exceeding 6 months
            self.declare_action("High Priority: Deploy Temporary Power Sources for Critical Facilities.")
        else:  # Moderate priority for shorter outages
            self.declare_action("Moderate Priority: Monitor Power Restoration Timelines.")

    @Rule(
    OR(
        BuildingAssessment(water_contamination=True),
        BuildingAssessment(water_access_disrupted=True)
    ))
    def water_sanitation_rule(self):
        if self.water_contamination:
            self.declare_action("Critical Priority: Immediate Water Sanitation Required.")
        elif self.water_access_disrupted:
            self.declare_action("Moderate Priority: Restore Water Supply Access.")
        else:
            self.declare_action("Low Priority: Monitor Water Supply Status.")
