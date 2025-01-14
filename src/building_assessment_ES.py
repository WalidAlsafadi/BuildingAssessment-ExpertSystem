from experta import *
import skfuzzy as fuzz
import numpy as np

# Define a fact class to represent building assessment data
class BuildingAssessment(Fact):
    """Fact schema for building assessment."""

    # Structural Factors
    sar_backscatter = Field(bool, default=False)  # Significant SAR backscatter decrease
    cracks = Field(str, default="none")  # Cracks: 'none', 'minor', 'moderate', 'severe'
    crack_confidence = Field(float, default=1.0)  # Confidence in crack assessment (0.0 to 1.0)
    load_bearing_cracks = Field(bool, default=False)  # Cracks in load-bearing walls
    load_confidence = Field(float, default=1.0)  # Confidence in load-bearing crack assessment (0.0 to 1.0)
    crack_width = Field(float, default=0.0)  # Width of cracks in mm
    width_confidence = Field(float, default=1.0)  # Confidence in crack width measurement (0.0 to 1.0)
    cracks_worsening = Field(bool, default=False)  # Minor cracks worsening over time
    worsening_confidence = Field(float, default=1.0)  # Confidence in worsening crack progression (0.0 to 1.0)
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
    slope_gradient = Field(float, default=0.0)  # Slope gradient in degrees (0 to 90)
    in_flood_zone = Field(bool, default=False)  # Is the building in a flood zone?
    flood_zone_proximity = Field(float, default=0.0) # Flood zone proximity
    flood_confidence = Field(float, default=1.0) # Confidence in flood zone (0.0 to 1.0)
    seismic_risk = Field(float, default=0.0)  # Peak Ground Acceleration (PGA) in g (0.0 to 1.0)
    seismic_confidence = Field(float, default=1.0) # Confidence in seismic risk (0.0 to 1.0)

    # Social Factors
    overcrowding = Field(bool, default=False)  # Is the building overcrowded?
    overcrowding_confidence = Field(float, default=1.0)  # Confidence in overcrowding assessment (0.0 to 1.0)
    vulnerable_population = Field(bool, default=False)  # Houses vulnerable groups (e.g., elderly, children)
    vulnerable_confidence = Field(float, default=1.0)  # Confidence in vulnerable population assessment (0.0 to 1.0)
    multiple_families = Field(bool, default=False)  # Building serves multiple families
    income_below_poverty = Field(bool, default=False)  # Owner's income is below the poverty threshold
    income_confidence = Field(float, default=1.0) # Confidence in Owner's income (0.0 to 1.0)
    population_displacement = Field(bool, default=False)  # Population displacement exceeding housing capacity
    temporary_shelter_needed = Field(bool, default=False)  # Displaced residents require temporary housing

    # Utility and Infrastructure
    damaged_utilities = Field(bool, default=False)  # Damaged sewer or water pipes
    utilities_confidence = Field(float, default=1.0)  # Confidence in damaged utilities assessment (0.0 to 1.0)
    access_to_power = Field(bool, default=False)  # Access to power reduces reconstruction priority
    critical_infrastructure = Field(bool, default=False)  # Is near critical infrastructure
    infrastructure_confidence = Field(float, default=1.0) # Confidence in critical infrastructure (0.0 to 1.0)
    power_outage_duration = Field(int, default=0)  # Duration of power outage in months
    water_contamination = Field(bool, default=False)  # Indicates bacterial or chemical contamination
    water_access_disrupted = Field(bool, default=False)  # Indicates temporary disruption to water access

    # Design and Data Availability
    outdated_design = Field(bool, default=False)  # Building design predates modern codes
    conflicting_data = Field(bool, default=False)  # Conflicting SAR and optical data
    missing_records = Field(bool, default=False)  # Missing pre- and post-war property records
    multiple_properties = Field(bool, default=False)  # Owner has multiple properties
    at_least_one_livable = Field(bool, default=False)  # At least one property is livable
    contaminated_materials = Field(bool, default=False)  # Indicates whether materials are contaminated
    renewable_energy_possible = Field(bool, default=False)  # Indicates feasibility of renewable energy integration

PRIORITY_MAP = {
    # Critical Actions
    "Critical: Reconstruction Delayed due to hazardous zone.": 100,
    "Critical: Reconstruction Delayed due to minefields.": 90,
    "Critical: Reconstruction Delayed due to landslide risk.": 100,
    "Critical: Earthquake reinforcement required.": 100,
    "Critical: Earthquake Reinforcement Required.": 95,
    "Critical: Prohibit rebuilding due to high radiation.": 95,
    "Critical: Immediate Repairs Required (SAR Detected).": 85,
    "Critical: Immediate Repairs Required (Visual Assessment).": 85,
    "Critical: Immediate Repairs Required for Load-Bearing Cracks.": 90,
    "Critical: Immediate Repairs Required for Severe Large Cracks.": 85,
    "Critical: Immediate Water Sanitation Required.": 85,
    "Critical: Combined impact of hazardous zone and overcrowding.": 100,
    "Critical: Combined Flood and Water Contamination Risk.": 100,
    "Critical: Prohibit rebuilding due to radiation and minefields.": 100,
    "Critical: Landslide Risk Near Critical Infrastructure in Hazardous zone.": 100,
    "Critical: Flood protection measures required.": 90,
    "Critical: Reconstruction Delayed due to High Flood Risk.": 95,
    "Critical: Combined risk of high radiation and cracks in hazardous zone.": 100,
    "Critical: Contaminated materials detected, remediation required.": 90,
    "Critical: Near critical infrastructure (e.g., hospitals, schools).": 100,

    # High-Priority Actions
    "High Priority: Combined risk of radiation and cracks.": 80,
    "High Priority: Vulnerable population safety.": 80,
    "High Priority: Immediate temporary housing needed for displaced residents.": 80,
    "High Priority: Restore Utilities for Vulnerable Population.": 85,
    "High Priority: Deploy Temporary Power Sources for Critical Facilities.": 85,
    "High Priority: Reconstruction due to overcrowding.": 75,
    "High Priority: Temporary housing near urban center for displaced residents.": 75,
    "High Priority: Deploy temporary power sources for critical facilities.": 90,
    "High Priority: Use pallet or container homes.": 70,
    "High Priority: Income below poverty threshold.": 70,
    "High Priority: Building serves multiple families.": 70,
    "High Priority: Clear road access before rebuilding.": 80,
    "High Priority: Hospitals or schools zone reconstruction.": 70,
    "High Priority: Combined impact of overcrowding and vulnerable population.": 85,
    "High Priority: Ensure utilities are restored for vulnerable population.": 80,
    "High Priority: Requires Field Validation.": 70,

    # Moderate Actions
    "Moderate: Flood zone and water contamination mitigation required.": 70,
    "Moderate: Repairs suggested for damaged utilities.": 50,
    "Moderate: Incorporate earthquake-resistant design.": 50,
    "Moderate: Proceed with caution due to landslide susceptibility.": 50,
    "Moderate: Flood protection measures required.": 50,
    "Moderate: Monitor timelines for power restoration.": 50,
    "Moderate: Restore water supply access.": 70,
    "Moderate: Monitor and mitigate radiation risks.": 65,
    "Moderate: Monitor landslide risk near critical infrastructure.": 70,

    # Recommendations and Low Priority Actions
    "Recommendation: Retrofit building to modern design standards.": 50,
    "Recommendation: Import certified materials to ensure safety.": 50,
    "Recommendation: Temporary housing near urban center.": 50,
    "Recommendation: Use geospatial data and neighboring properties for estimation.": 50,
    "Recommendation: Routine repairs recommended.": 30,
    "Low Priority: Landslide risk is minimal.": 30,
    "Low Priority: Flood risk is minimal.": 30,
    "Low Priority: Seismic risk is minimal.": 30,
    "Low Priority: Radiation levels are within safe limits.": 20,
    "Low Priority: No immediate repairs required (Radar stable).": 20,
    "Low Priority: At least one livable property available.": 20,
    "Low Priority: Energy resource allocation not required.": 20,
    "Low Priority: Routine Repairs Recommended.": 20,
    "Lower Priority: At least one livable property available.": 20,
}

CRACK_SEVERITY_MAP = {
    "none": 0,
    "minor": 3,
    "moderate": 6,
    "severe": 10
}

class BuildingAssessmentExpertSystem(KnowledgeEngine):
    """
    Rule-based expert system for evaluating building conditions using fuzzy logic
    and prioritizing actions based on confidence values. Includes backward chaining.
    """

    def __init__(self):
        super().__init__()
        self.prioritized_actions = []

        # Define fuzzy membership functions
        self.x_cracks = np.arange(0, 11, 1)
        self.minor_cracks = fuzz.trimf(self.x_cracks, [0, 0, 4])
        self.moderate_cracks = fuzz.trimf(self.x_cracks, [4, 6, 8])
        self.severe_cracks = fuzz.trimf(self.x_cracks, [7, 10, 10])

        self.x_confidence = np.arange(0.0, 1.1, 0.1)
        self.low_confidence = fuzz.trimf(self.x_confidence, [0.0, 0.0, 0.4])
        self.moderate_confidence = fuzz.trimf(self.x_confidence, [0.3, 0.6, 0.8])
        self.high_confidence = fuzz.trimf(self.x_confidence, [0.7, 1.0, 1.0])

    def evaluate_fuzzy_membership(self, value, x_range, membership_function, verbose=False):
        """
        Evaluate the degree of membership of a value in a fuzzy set.
        
        Args:
            value (float): Input value to evaluate.
            x_range (array): The range of the fuzzy variable.
            membership_function (array): Membership function of the fuzzy set.
            verbose (bool): If True, prints debug information.
            
        Returns:
            float: Membership value (0.0 to 1.0).
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Error: Invalid value type {type(value)} for fuzzy membership evaluation.")
        if value < x_range[0] or value > x_range[-1]:
            raise ValueError(f"Value {value} is outside the range of the fuzzy variable.")
        membership = fuzz.interp_membership(x_range, membership_function, value)
        if verbose:
            print(f"Value: {value}, Membership: {membership}")
        return membership

    def declare_action(self, action, confidence=1.0):
        """
        Declares an action with a scaled priority based on confidence.
        - If confidence is 1.0, the full priority is used.
        - Lower confidence scales down the priority proportionally.
        """
        # Avoid duplicate actions
        if any(a[1] == action for a in self.prioritized_actions):
            return
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

    def get_top_actions(self, top_n=5, verbose=False):
        """
        Returns the top `n` prioritized actions as a list of tuples.
        Each tuple contains (priority, action).
        """
        self.prioritized_actions.sort(reverse=True, key=lambda x: x[0])
        if verbose:
            return [(priority, f"Action: {action}") for priority, action in self.prioritized_actions[:top_n]]
        return self.prioritized_actions[:top_n]

    def validate_confidence(self, conf):
        """
        Validates the confidence value provided for a rule or fact.

        Args:
            conf (float or None): The confidence value to validate, expected to be between 0.0 and 1.0.

        Returns:
            float: The validated confidence value. If the input is None or out of range, defaults to 1.0.
        """
        return conf if conf is not None and 0.0 <= conf <= 1.0 else 1.0

    def backward_chain(self, goal_action):
        """
        Perform backward chaining to achieve a goal action.

        Args:
            goal_action (str): The desired action to achieve.

        Returns:
            bool: True if the goal action is achieved, False otherwise.
        """
        for rule in self.rules:
            if rule['action'] == goal_action:
                # Evaluate conditions of the rule
                for condition in rule['conditions']:
                    if not self.evaluate_condition(condition):
                        print(f"Condition '{condition}' for goal '{goal_action}' not satisfied.")
                        return False
                print(f"Goal '{goal_action}' achieved via rule: {rule['name']}")
                return True
        print(f"Goal '{goal_action}' could not be achieved.")
        return False

    def evaluate_condition(self, condition):
        """
        Evaluate a single condition. If the condition is not a fact, recursively check subgoals.

        Args:
            condition (str): The condition to evaluate.

        Returns:
            bool: True if the condition is satisfied, False otherwise.
        """
        # Check if the condition exists in facts
        if condition in self.facts:
            return self.facts[condition]

        # Check if the condition is derived from another rule
        for rule in self.rules:
            if condition in rule['action']:
                print(f"Evaluating subgoal: {condition}")
                return self.backward_chain(rule['action'])

        # If the condition is not resolved, check the default "facts" dictionary
        print(f"Condition '{condition}' not explicitly provided. Checking default responses.")
        return self.default_facts.get(condition, False)


    ### Structural Damage Assessment Rules ###

    @Rule(BuildingAssessment(sar_backscatter=True))
    def severe_sar_damage(self):
        self.declare_action("Critical: Immediate Repairs Required (SAR Detected).")

    @Rule(BuildingAssessment(cracks=MATCH.crack_severity, crack_confidence=MATCH.conf))
    def fuzzy_crack_severity_rule(self, crack_severity, conf):
        crack_severity_value = CRACK_SEVERITY_MAP.get(crack_severity, 0)
        crack_severe = self.evaluate_fuzzy_membership(crack_severity_value, self.x_cracks, self.severe_cracks)
        if crack_severe > 0.7 and conf > 0.7:
            self.declare_action("Critical: Immediate Repairs Required (Visual Assessment).", confidence=min(crack_severe, conf))

    @Rule(BuildingAssessment(load_bearing_cracks=True, crack_width=0.0, load_confidence=MATCH.conf))
    def load_bearing_cracks_rule(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.9:
            self.declare_action("Critical: Immediate Repairs Required for Load-Bearing Cracks.", confidence=conf)

    @Rule(BuildingAssessment(cracks="moderate", crack_confidence=MATCH.conf))
    def moderate_cracks_with_confidence(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.6:
            self.declare_action("Moderate: Repairs Suggested.", confidence=conf)

    @Rule(BuildingAssessment(cracks="minor", crack_confidence=MATCH.conf))
    def minor_surface_cracks_with_confidence(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.5:
            self.declare_action("Low Priority: Routine Repairs Recommended.", confidence=conf)

    @Rule(BuildingAssessment(crack_width=MATCH.width, width_confidence=MATCH.conf))
    def severe_large_crack_rule(self, width, conf):
        conf = self.validate_confidence(conf)
        if width >= 20.0 and conf >= 0.9:
            self.declare_action("Critical: Immediate Repairs Required for Severe Large Cracks.", confidence=conf)

    @Rule(BuildingAssessment(cracks_worsening=True, worsening_confidence=MATCH.conf))
    def worsening_cracks_priority_with_confidence(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.8:
            self.declare_action("Moderate: Cracks worsening over time.", confidence=conf)

    ### Environmental Hazard Rules ###

    @Rule(
        AND(
            BuildingAssessment(hazardous_zone=True, hazardous_confidence=MATCH.conf),
            NOT(Fact(slope_gradient=W()))  # Exclude cases where slope is defined
        )
    )
    def hazardous_zone_with_uncertainty(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.6:
            self.declare_action("Critical: Reconstruction Delayed due to hazardous zone.", confidence=conf)

    @Rule(BuildingAssessment(radiation_level=MATCH.radiation, radiation_confidence=MATCH.conf))
    def radiation_rule_with_confidence(self, radiation, conf):
        conf = self.validate_confidence(conf)
        if radiation > 20.0:  # High radiation
            self.declare_action("Critical: Prohibit rebuilding due to high radiation.", confidence=conf)
        elif 1.0 < radiation <= 20.0:  # Moderate radiation
            self.declare_action("Moderate: Monitor and mitigate radiation risks.", confidence=conf)
        elif 0 < radiation <= 1.0:  # Safe radiation
            self.declare_action("Low Priority: Radiation levels are within safe limits.", confidence=conf)

    @Rule(BuildingAssessment(water_contamination=True))
    def individual_water_contamination_rule(self):
        self.declare_action("Critical: Immediate Water Sanitation Required.")

    @Rule(BuildingAssessment(unexploded_ordnance=True, ordnance_confidence=MATCH.conf))
    def minefields_with_uncertainty(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.75:
            self.declare_action("Critical: Reconstruction Delayed due to minefields.", confidence=conf)

    @Rule(BuildingAssessment(contaminated_materials=True))
    def contaminated_materials_priority(self):
        self.declare_action("Critical: Contaminated materials detected, remediation required.")

    @Rule(BuildingAssessment(flood_zone_proximity=MATCH.distance, flood_confidence=MATCH.conf))
    def flood_zone_proximity_rule(self, distance, conf):
        conf = self.validate_confidence(conf)
        if distance >= 500.0 and conf >= 0.7:
            self.declare_action("Critical: Reconstruction Delayed due to High Flood Risk.", confidence=conf)
        elif 100.0 <= distance < 500.0 and conf >= 0.5:
            self.declare_action("Moderate: Flood Protection Measures Required.", confidence=conf)
        elif distance > 0.0 and conf >= 0.4:
            self.declare_action("Low Priority: Flood risk is minimal.", confidence=conf)

    @Rule(BuildingAssessment(seismic_risk=MATCH.pga, seismic_confidence=MATCH.conf))
    def seismic_activity_rule(self, pga, conf):
        conf = self.validate_confidence(conf)
        if pga > 0.4 and conf >= 0.7:
            self.declare_action("Critical: Earthquake Reinforcement Required.", confidence=conf)
        elif 0.2 < pga <= 0.4 and conf >= 0.5:
            self.declare_action("Moderate: Incorporate Earthquake-Resistant Design.", confidence=conf)

    @Rule(BuildingAssessment(in_flood_zone=True, flood_confidence=MATCH.conf))
    def flood_zone_rule(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.7:
            self.declare_action("Critical: Flood protection measures required.", confidence=conf)
        elif conf >= 0.5:
            self.declare_action("Moderate: Monitor flood risks and prepare mitigation strategies.", confidence=conf)

    @Rule(BuildingAssessment(slope_gradient=MATCH.slope))
    def slope_gradient_rule(self, slope):
        if slope > 30:
            self.declare_action("Critical: Reconstruction Delayed due to landslide risk.")
        elif 15 < slope <= 30:
            self.declare_action("Moderate: Landslide risk present. Monitor closely.")
        elif slope > 0:
            self.declare_action("Low Priority: Minimal landslide risk.")

    @Rule(BuildingAssessment(water_access_disrupted=True))
    def water_access_disruption_rule(self):
        self.declare_action("Moderate: Restore water access as soon as possible.")

    ### Data and Assessment Rules ###

    @Rule(BuildingAssessment(significant_difference=True))
    def significant_differences_priority(self):
        self.declare_action("Moderate: Further Inspection Needed.")

    @Rule(BuildingAssessment(conflicting_data=True))
    def conflicting_data_priority(self):
        self.declare_action("High Priority: Requires Field Validation.")

    @Rule(BuildingAssessment(missing_records=True))
    def use_geospatial_data(self):
        self.declare_action("Recommendation: Use geospatial data and neighboring properties for estimation.")
    
    @Rule(BuildingAssessment(radar_stable=True))
    def stable_radar_rule(self):
        self.declare_action("Low Priority: No immediate repairs required (Radar stable).")

    ### Social Factors Rules ###

    @Rule(BuildingAssessment(overcrowding=True, overcrowding_confidence=MATCH.conf))
    def overcrowding_with_uncertainty(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.7:
            self.declare_action("High Priority: Reconstruction due to overcrowding.", confidence=conf)

    @Rule(BuildingAssessment(vulnerable_population=True, vulnerable_confidence=MATCH.conf))
    def vulnerable_population_with_uncertainty(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.8:
            self.declare_action("High Priority: Vulnerable population safety.", confidence=conf)

    @Rule(BuildingAssessment(population_displacement=True))
    def population_displacement_priority(self):
        self.declare_action("High Priority: Use pallet or container homes.")

    @Rule(BuildingAssessment(income_below_poverty=True, income_confidence=MATCH.conf))
    def income_priority(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.7:
            self.declare_action("High Priority: Income below poverty threshold.", confidence=conf)

    @Rule(BuildingAssessment(multiple_families=True))
    def prioritize_multiple_families(self):
        self.declare_action("High Priority: Building serves multiple families.")

    @Rule(BuildingAssessment(at_least_one_livable=True))
    def deprioritize_livable_properties(self):
        self.declare_action("Lower Priority: At least one livable property available.")

    ### Design and Sustainability Rules ###

    @Rule(BuildingAssessment(outdated_design=True))
    def recommend_retrofitting(self):
        self.declare_action("Recommendation: Retrofit building to modern design standards.")

    @Rule(BuildingAssessment(renewable_energy_possible=True))
    def renewable_energy_integration(self):
        self.declare_action("Recommendation: Integrate renewable energy systems.")
 
    ### Utility and Infrastructure Rules ###

    @Rule(
        AND(
            BuildingAssessment(critical_infrastructure=True, infrastructure_confidence=MATCH.conf),
            NOT(Fact(power_outage_duration=W()))  # Ensure no power outage duration is provided
        )
    )
    def critical_infrastructure_priority(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.8:  # High confidence threshold
            self.declare_action("Critical: Near critical infrastructure (e.g., hospitals, schools).", confidence=conf)

    @Rule(BuildingAssessment(damaged_utilities=True, utilities_confidence=MATCH.conf))
    def damaged_utilities_with_uncertainty(self, conf):
        conf = self.validate_confidence(conf)
        if conf >= 0.8:
            self.declare_action("Moderate: Repairs suggested for damaged utilities.", confidence=conf)

    @Rule(BuildingAssessment(access_to_power=True))
    def lower_priority_energy(self):
        self.declare_action("Low Priority: Energy resource allocation not required.")

    @Rule(BuildingAssessment(road_inaccessibility=True))
    def road_inaccessibility_priority(self):
        self.declare_action("High Priority: Clear road access before rebuilding.")

    @Rule(BuildingAssessment(urban_proximity=True))
    def urban_proximity_rule(self):
        self.declare_action("Recommendation: Prioritize urban-center buildings for temporary housing.")

    @Rule(BuildingAssessment(temporary_shelter_needed=True))
    def temporary_shelter_rule(self):
        self.declare_action("High Priority: Immediate temporary housing needed for displaced residents.")

    @Rule((BuildingAssessment(power_outage_duration=MATCH.duration)))
    def temporary_power_rule(self, duration):
        if duration > 6:  # High priority for outages exceeding 6 months
            self.declare_action("High Priority: Deploy Temporary Power Sources for Critical Facilities.")
            for fact in list(self.facts.values()):
                if isinstance(fact, BuildingAssessment):
                    self.retract(fact)
        elif 0 < duration <= 6:  # Moderate priority for shorter outages
            self.declare_action("Moderate: Monitor Power Restoration Timelines.")
            for fact in list(self.facts.values()):
                if isinstance(fact, BuildingAssessment):
                    self.retract(fact)


    ### Combined Rules ###

    @Rule(AND(
        BuildingAssessment(radiation_level=MATCH.radiation, radiation_confidence=MATCH.radiation_conf),
        BuildingAssessment(unexploded_ordnance=True, ordnance_confidence=MATCH.ordnance_conf)
        ))
    def radiation_and_minefields(self, radiation, radiation_conf, ordnance_conf):
        combined_conf = min(radiation_conf, ordnance_conf)
        if radiation > 1.0 and combined_conf >= 0.75:
            self.declare_action("Critical: Prohibit rebuilding due to radiation and minefields.", confidence=combined_conf)
            # Suppress individual outputs
            for fact in list(self.facts.values()):
                if isinstance(fact, BuildingAssessment):
                    self.retract(fact)

    @Rule(
        AND(
            BuildingAssessment(hazardous_zone=True, hazardous_confidence=MATCH.conf),
            BuildingAssessment(slope_gradient=MATCH.slope),
            BuildingAssessment(critical_infrastructure=MATCH.critical_infrastructure)
        )
    )
    def landslide_risk_rule(self, conf, slope):
        conf = self.validate_confidence(conf)
        if slope > 30 and conf >= 0.6:
            self.declare_action("Critical: Landslide Risk Near Critical Infrastructure in Hazardous zone.", confidence=conf)
            for fact in list(self.facts.values()):
                if isinstance(fact, BuildingAssessment):
                    self.retract(fact)
        elif 20 < slope <= 30 and conf >= 0.5:
                self.declare_action("Moderate: Monitor landslide risk near critical infrastructure.", confidence=conf)
                for fact in list(self.facts.values()):
                    if isinstance(fact, BuildingAssessment):
                        self.retract(fact)
        elif slope > 0:
            self.declare_action("Low Priority: Landslide risk is minimal.", confidence=conf)
            for fact in list(self.facts.values()):
                    if isinstance(fact, BuildingAssessment):
                        self.retract(fact)

    @Rule(
            AND(
                BuildingAssessment(hazardous_zone=True, hazardous_confidence=MATCH.hazardous_conf),
                BuildingAssessment(overcrowding=True, overcrowding_confidence=MATCH.overcrowding_conf)
            )
        )
    def hazardous_zone_and_overcrowding_rule(self, hazardous_conf, overcrowding_conf):
        combined_conf = min(hazardous_conf, overcrowding_conf)
        if combined_conf >= 0.7:
            self.declare_action("Critical: Combined impact of hazardous zone and overcrowding.", confidence=combined_conf)
            # Suppress individual outputs
            for fact in list(self.facts.values()):
                if isinstance(fact, BuildingAssessment):
                    self.retract(fact)
                    
    @Rule(
        AND(
            BuildingAssessment(radiation_level=MATCH.radiation, radiation_confidence=MATCH.radiation_conf),
            BuildingAssessment(cracks=MATCH.crack_severity, crack_confidence=MATCH.crack_conf),
            BuildingAssessment(hazardous_zone=True, hazardous_confidence=MATCH.hazardous_conf)
        )
    )
    def combined_radiation_and_cracks_rule(self, radiation, radiation_conf, crack_severity, crack_conf, hazardous_conf):
        combined_conf = min(radiation_conf, crack_conf, hazardous_conf)

        if radiation > 2.0 and combined_conf >= 0.7:
            self.declare_action(
                "Critical: Combined risk of high radiation and cracks in hazardous zone.",
                confidence=combined_conf
            )
            for fact in list(self.facts.values()):
                if isinstance(fact, BuildingAssessment):
                    self.retract(fact)

    @Rule(
        AND(
            BuildingAssessment(flood_zone_proximity=MATCH.proximity),
            BuildingAssessment(water_contamination=True)
        )
    )
    def flood_zone_and_water_contamination_rule(self, proximity):
        if proximity >= 100:
            self.declare_action("Critical: Combined Flood and Water Contamination Risk.")

        # Suppress individual facts
        facts_to_retract = []
        for fact in list(self.facts.values()):
            if isinstance(fact, BuildingAssessment):
                if fact.get("flood_zone_proximity") == proximity or fact.get("water_contamination") is True:
                    facts_to_retract.append(fact)

        for fact in facts_to_retract:
            try:
                self.retract(fact)
            except Exception:
                pass


    @Rule(
        AND(
        BuildingAssessment(urban_proximity=True),
        BuildingAssessment(temporary_shelter_needed=True)
        )
    )
    def urban_temporary_shelter(self):
        self.declare_action("High Priority: Temporary housing near urban center for displaced residents.")
        for fact in list(self.facts.values()):
            if isinstance(fact, BuildingAssessment):
                self.retract(fact)

    @Rule(
        AND(
            BuildingAssessment(vulnerable_population=True, vulnerable_confidence=MATCH.vulnerable_conf),
            BuildingAssessment(damaged_utilities=True, utilities_confidence=MATCH.utilities_conf)
        )
    )
    def vulnerable_population_and_damaged_utilities_rule(self, vulnerable_conf, utilities_conf):
        combined_conf = min(vulnerable_conf, utilities_conf)  # Use the lower confidence level
        if combined_conf >= 0.8:  # High confidence threshold
            self.declare_action("High Priority: Restore Utilities for Vulnerable Population.", confidence=combined_conf)
            # Suppress individual outputs
            for fact in list(self.facts.values()):
                if isinstance(fact, BuildingAssessment):
                    self.retract(fact)

    @Rule(
        AND(
            BuildingAssessment(water_contamination=MATCH.water_contamination),
            BuildingAssessment(water_access_disrupted=MATCH.water_access_disrupted)
        )
    )
    def water_sanitation_rule(self, water_contamination=None, water_access_disrupted=None):
        if water_contamination and water_access_disrupted:
            self.declare_action("Critical: Immediate Water Sanitation Required.")
            for fact in list(self.facts.values()):
                if isinstance(fact, BuildingAssessment):
                    self.retract(fact)

### Zero Confidence Rule ###

    @Rule(
        AND(
            OR(
                BuildingAssessment(crack_confidence=MATCH.crack_conf),
                BuildingAssessment(load_confidence=MATCH.load_conf),
                BuildingAssessment(width_confidence=MATCH.width_conf),
                BuildingAssessment(worsening_confidence=MATCH.worsening_conf),
                BuildingAssessment(ordnance_confidence=MATCH.ordnance_conf),
                BuildingAssessment(flood_confidence=MATCH.flood_conf),
                BuildingAssessment(seismic_confidence=MATCH.seismic_conf),
                BuildingAssessment(vulnerable_confidence=MATCH.vulnerable_conf),
                BuildingAssessment(income_confidence=MATCH.income_conf),
                BuildingAssessment(utilities_confidence=MATCH.utilities_conf),
                BuildingAssessment(hazardous_confidence=MATCH.hazardous_conf),
                BuildingAssessment(radiation_confidence=MATCH.radiation_conf),
                BuildingAssessment(infrastructure_confidence=MATCH.infrastructure_conf),
                BuildingAssessment(overcrowding_confidence=MATCH.overcrowding_conf),
            ),
            NOT(Fact(prioritized_action=W()))  # Ensure no actions exist yet
        )
    )
    def zero_confidence_rule(self, crack_conf=None, load_conf=None, width_conf=None, worsening_conf=None, ordnance_conf=None,
                            flood_conf=None, seismic_conf=None, vulnerable_conf=None, income_conf=None, utilities_conf=None,
                            hazardous_conf=None, radiation_conf=None, infrastructure_conf=None, overcrowding_conf=None):
        # Check if all provided confidence values are zero
        confidence_values = [
            crack_conf, load_conf, width_conf, worsening_conf, ordnance_conf,
            flood_conf, seismic_conf, vulnerable_conf, income_conf, utilities_conf,
            hazardous_conf, radiation_conf, infrastructure_conf, overcrowding_conf
        ]
        
        if all(conf == 0.0 for conf in confidence_values if conf is not None):
            self.declare_action(
                "Recommendation: Further inspection required due to zero confidence.",
                confidence=0.5
            )
