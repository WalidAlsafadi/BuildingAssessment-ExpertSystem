import streamlit as st
from building_assessment_ES import BuildingAssessment, BuildingAssessmentExpertSystem

# Header Section
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        color: dodgerBlue;
        font-weight: bold;
        text-align: center;
    }
    .subtitle {
        font-size: 18px;
        color: White;
        text-align: center;
    }
    .footer {
        font-size: 14px;
        color: #7f8c8d;
        text-align: center;
        padding: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="title">Building Assessment Expert System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">'
    "A decision-support tool for prioritizing actions on post-war building conditions "
    "using rule-based reasoning and fuzzy logic."
    "</div>", unsafe_allow_html=True
)

st.divider()

# Section: Structural Damage Assessment
st.header("Structural Damage Assessment")
st.caption("Evaluate structural factors such as cracks, load-bearing issues, and worsening conditions.")

# Severe SAR backscatter
sar_backscatter = st.checkbox(
    "Severe SAR backscatter detected?",
    help="Indicates significant structural deformation based on SAR analysis."
)

# Cracks in the building
has_cracks = st.checkbox("Does the building have cracks?")
cracks = "none"  # Default value
crack_confidence = 1.0  # Default confidence value

if has_cracks:
    cracks = st.selectbox(
        "Type of cracks:",
        ["minor", "moderate", "severe"],
        help="Classify the cracks based on their severity."
    )
    crack_confidence = st.number_input(
        "Confidence in crack assessment (0.0 - 1.0):",
        min_value=0.0, max_value=1.0, value=1.0,
        help="Enter your confidence in the crack assessment."
    )

    # Load-bearing cracks
    load_bearing_cracks = st.checkbox(
        "Cracks in load-bearing walls?",
        help="Select if the cracks affect load-bearing walls."
    )
    load_confidence = 1.0
    if load_bearing_cracks:
        load_confidence = st.number_input(
            "Confidence in load-bearing cracks assessment (0.0 - 1.0):",
            min_value=0.0, max_value=1.0, value=1.0,
            help="Enter your confidence in load-bearing cracks assessment."
        )

    # Crack width
    crack_width = st.number_input(
        "Width of cracks (mm):",
        min_value=0.0, value=0.0,
        help="Specify the measured width of the cracks in millimeters."
    )
    width_confidence = 1.0
    if crack_width > 0.0:
        width_confidence = st.number_input(
            "Confidence in crack width measurement (0.0 - 1.0):",
            min_value=0.0, max_value=1.0, value=1.0,
            help="Enter your confidence in the crack width measurement."
        )

    # Worsening cracks
    cracks_worsening = st.checkbox(
        "Are the cracks worsening over time?",
        help="Select if minor cracks are worsening over time."
    )
    worsening_confidence = 1.0
    if cracks_worsening:
        worsening_confidence = st.number_input(
            "Confidence in worsening cracks assessment (0.0 - 1.0):",
            min_value=0.0, max_value=1.0, value=1.0,
            help="Enter your confidence in the worsening cracks assessment."
        )
else:
    # Default values if no cracks are selected
    load_bearing_cracks = False
    load_confidence = 1.0
    crack_width = 0.0
    width_confidence = 1.0
    cracks_worsening = False
    worsening_confidence = 1.0

st.divider()

# Section: Environmental Hazard Assessment
st.header("Environmental Hazard Assessment")
st.caption("Evaluate environmental risks such as hazardous zones, radiation, ordnance, and proximity to flood zones.")

# Hazardous Zone
hazardous_zone = st.checkbox(
    "Is the building in a hazardous zone?",
    help="Select this if the building is located in an area with environmental risks (e.g., flooding, radiation)."
)
hazardous_confidence = 1.0  # Default confidence value
if hazardous_zone:
    hazardous_confidence = st.number_input(
        "Confidence in hazardous zone assessment (0.0 - 1.0):",
        min_value=0.0, max_value=1.0, value=1.0,
        help="Enter your confidence in the hazardous zone assessment."
    )

# Radiation Risk
radiation_detected = st.checkbox(
    "Is there a radiation risk?",
    help="Select this if radiation levels in the area are a concern."
)
radiation_level = 0.0
radiation_confidence = 1.0
if radiation_detected:
    radiation_level = st.number_input(
        "Radiation Level (mSv/year):",
        min_value=0.0, value=0.0,
        help="Specify the measured radiation level in millisieverts per year."
    )
    radiation_confidence = st.number_input(
        "Confidence in radiation assessment (0.0 - 1.0):",
        min_value=0.0, max_value=1.0, value=1.0,
        help="Enter your confidence in the radiation level measurement."
    )

# Unexploded Ordnance
unexploded_ordnance = st.checkbox(
    "Are there nearby minefields or unexploded ordnance?",
    help="Select this if the area contains minefields or unexploded ordnance."
)
ordnance_confidence = 1.0
if unexploded_ordnance:
    ordnance_confidence = st.number_input(
        "Confidence in ordnance detection (0.0 - 1.0):",
        min_value=0.0, max_value=1.0, value=1.0,
        help="Enter your confidence in the ordnance detection."
    )

# Contaminated Materials
contaminated_materials = st.checkbox(
    "Are contaminated materials detected?",
    help="Select this if the building materials are contaminated and unsafe."
)

# Flood Zone
in_flood_zone = st.checkbox(
    "Is the building in a flood zone?",
    help="Select this if the building is located in a flood-prone area."
)

flood_zone_proximity = 0.0  # Default proximity
flood_confidence = 1.0  # Default confidence

if in_flood_zone:
    flood_zone_proximity = st.number_input(
        "Distance to nearest flood zone (meters):",
        min_value=0.0, value=0.0,
        help="Specify the distance from the building to the nearest flood zone in meters."
    )
    flood_confidence = st.number_input(
        "Confidence in flood zone assessment (0.0 - 1.0):",
        min_value=0.0, max_value=1.0, value=1.0,
        help="Enter your confidence in the flood zone assessment."
    )


# Slope Gradient
land_risk = st.checkbox(
    "Is there a slope or land risk?",
    help="Select this if the building is located near a sloped area."
)
slope_gradient = 0.0
if land_risk:
    slope_gradient = st.number_input(
        "Slope Gradient (degrees):",
        min_value=0.0, max_value=90.0, value=0.0,
        help="Specify the slope gradient near the building in degrees."
    )

# Seismic Risk
seismic_detected = st.checkbox(
    "Is there a seismic risk?",
    help="Select this if the area has a potential for earthquakes."
)
seismic_risk = 0.0
seismic_confidence = 1.0
if seismic_detected:
    seismic_risk = st.number_input(
        "Seismic Risk (PGA in g):",
        min_value=0.0, max_value=1.0, value=0.0,
        help="Specify the Peak Ground Acceleration (PGA) representing seismic risk."
    )
    seismic_confidence = st.number_input(
        "Confidence in seismic risk assessment (0.0 - 1.0):",
        min_value=0.0, max_value=1.0, value=1.0,
        help="Enter your confidence in the seismic risk assessment."
    )

st.divider()

# Section: Social and Infrastructure Assessment
st.header("Social and Infrastructure Assessment")
st.caption("Assess social impact, overcrowding, and proximity to critical infrastructure.")

# Overcrowding
overcrowding = st.checkbox(
    "Is the building overcrowded?",
    help="Select this if the building is overcrowded beyond its capacity."
)
overcrowding_confidence = 1.0
if overcrowding:
    overcrowding_confidence = st.number_input(
        "Confidence in overcrowding assessment (0.0 - 1.0):",
        min_value=0.0, max_value=1.0, value=1.0,
        help="Enter your confidence in the overcrowding assessment."
    )

# Vulnerable Population
vulnerable_population = st.checkbox(
    "Does the building house vulnerable groups?",
    help="Select this if the building houses vulnerable populations (e.g., elderly, children)."
)
vulnerable_confidence = 1.0
if vulnerable_population:
    vulnerable_confidence = st.number_input(
        "Confidence in vulnerable population assessment (0.0 - 1.0):",
        min_value=0.0, max_value=1.0, value=1.0,
        help="Enter your confidence in the vulnerable population assessment."
    )

# Critical Infrastructure
critical_infrastructure = st.checkbox(
    "Is the building near critical infrastructure?",
    help="Select this if the building is close to critical infrastructure like hospitals or schools."
)
infrastructure_confidence = 1.0
if critical_infrastructure:
    infrastructure_confidence = st.number_input(
        "Confidence in critical infrastructure proximity (0.0 - 1.0):",
        min_value=0.0, max_value=1.0, value=1.0,
        help="Enter your confidence in proximity to critical infrastructure."
    )

# Population Displacement
population_displacement = st.checkbox(
    "Does the population displacement exceed housing capacity?",
    help="Select this if the displaced population exceeds available permanent housing."
)

# Multiple Families
multiple_families = st.checkbox(
    "Does the building serve multiple families?",
    help="Select this if the building serves as a residence for multiple families."
)

# Income Below Poverty
income_below_poverty = st.checkbox(
    "Is the income level below the poverty threshold?",
    help="Select this if the income level of residents is below the poverty threshold."
)
income_confidence = 1.0
if income_below_poverty:
    income_confidence = st.number_input(
        "Confidence in income assessment (0.0 - 1.0):",
        min_value=0.0, max_value=1.0, value=1.0,
        help="Enter your confidence in the income level assessment."
    )

st.divider()

# Section: Design and Sustainability Considerations
st.header("Design and Sustainability Considerations")
st.caption("Explore the feasibility of modern design standards, renewable energy integration, and temporary housing needs.")

# Outdated Design
outdated_design = st.checkbox(
    "Does the building design predate modern codes?",
    help="Select this if the building was designed before modern construction standards."
)

# Renewable Energy Feasibility
renewable_energy_possible = st.checkbox(
    "Is renewable energy integration feasible?",
    help="Select this if the building can integrate renewable energy systems."
)

# Temporary Shelter Needed
temporary_shelter_needed = st.checkbox(
    "Are displaced residents requiring temporary housing?",
    help="Select this if the displaced residents require immediate temporary housing."
)

# At Least One Livable Property
at_least_one_livable = st.checkbox(
    "Is at least one property livable?",
    help="Select this if at least one of the owner's properties is livable."
)

st.divider()

# Section: Data and Utility Analysis
st.header("Data and Utility Analysis")
st.caption("Analyze utility damage, accessibility, and data inconsistencies for informed decisions.")

# Significant Differences
significant_difference = st.checkbox(
    "Significant differences in damage assessments?",
    help="Select this if multiple damage assessments significantly differ."
)

# Conflicting Data
conflicting_data = st.checkbox(
    "Are there conflicting SAR and optical data?",
    help="Select this if remote sensing data (SAR vs. optical) shows conflicting results."
)

# Missing Records
missing_records = st.checkbox(
    "Are pre- and post-war property records missing?",
    help="Select this if historical records are unavailable."
)

# Damaged Utilities
damaged_utilities = st.checkbox(
    "Are there damaged sewer or water pipes?",
    help="Select this if the building's utilities (e.g., sewer, water pipes) are damaged."
)
utilities_confidence = 1.0
if damaged_utilities:
    utilities_confidence = st.number_input(
        "Confidence in damaged utilities assessment (0.0 - 1.0):",
        min_value=0.0, max_value=1.0, value=1.0,
        help="Enter your confidence in the damaged utilities assessment."
    )

# Access to Power
access_to_power = st.checkbox(
    "Does the building have access to power?",
    help="Select this if the building has reliable access to power."
)

# Road Inaccessibility
road_inaccessibility = st.checkbox(
    "Are roads to the building inaccessible?",
    help="Select this if road access to the building is blocked or damaged."
)

# Power Outage Duration
has_power_outage = st.checkbox(
    "Is there a power outage?",
    help="Select this if the building has experienced a power outage."
)
power_outage_duration = 0  # Default value
if has_power_outage:
    power_outage_duration = st.number_input(
        "Duration of power outage (months):",
        min_value=0, value=0,
        help="Specify the duration of the power outage in months."
    )

# Water Contamination
water_contamination = st.checkbox(
    "Is water contamination detected?",
    help="Select this if bacterial or chemical contamination in water is detected."
)

# Water Access Disruption
water_access_disrupted = st.checkbox(
    "Is water access temporarily disrupted?",
    help="Select this if water access to the building is temporarily disrupted."
)

st.divider()

# Run Expert System
if st.button("Run Expert System"):
    # Initialize the expert system
    engine = BuildingAssessmentExpertSystem()
    engine.reset()

    # Declare facts for structural assessment
    engine.declare(
        BuildingAssessment(
            #Structural Inputs
            sar_backscatter=sar_backscatter,
            cracks=cracks,
            crack_confidence=crack_confidence,
            load_bearing_cracks=load_bearing_cracks,
            load_confidence=load_confidence,
            crack_width=crack_width,
            width_confidence=width_confidence,
            cracks_worsening=cracks_worsening,
            worsening_confidence=worsening_confidence,

            # Environmental Inputs
            hazardous_zone=hazardous_zone,
            hazardous_confidence=hazardous_confidence,
            radiation_level=radiation_level,
            radiation_confidence=radiation_confidence,
            unexploded_ordnance=unexploded_ordnance,
            ordnance_confidence=ordnance_confidence,
            contaminated_materials=contaminated_materials,
            in_flood_zone=in_flood_zone,
            flood_confidence=flood_confidence,
            flood_zone_proximity=flood_zone_proximity,
            slope_gradient=slope_gradient,
            seismic_risk=seismic_risk,
            seismic_confidence=seismic_confidence,

            # Social Inputs
            overcrowding=overcrowding,
            overcrowding_confidence=overcrowding_confidence,
            vulnerable_population=vulnerable_population,
            vulnerable_confidence=vulnerable_confidence,
            critical_infrastructure=critical_infrastructure,
            infrastructure_confidence=infrastructure_confidence,
            population_displacement=population_displacement,
            multiple_families=multiple_families,
            income_below_poverty=income_below_poverty,
            income_confidence=income_confidence,

            # Design and Sustainability Inputs
            outdated_design=outdated_design,
            renewable_energy_possible=renewable_energy_possible,
            temporary_shelter_needed=temporary_shelter_needed,
            at_least_one_livable=at_least_one_livable,

            # Data and Utility Inputs
            significant_difference=significant_difference,
            conflicting_data=conflicting_data,
            missing_records=missing_records,
            damaged_utilities=damaged_utilities,
            utilities_confidence=utilities_confidence,
            access_to_power=access_to_power,
            road_inaccessibility=road_inaccessibility,
            power_outage_duration=power_outage_duration,
            water_contamination=water_contamination,
            water_access_disrupted=water_access_disrupted
        )
    )

    # Run the engine
    engine.run()

    # Display results
    st.subheader("Results")
    if engine.prioritized_actions:
        st.success("Analysis complete. Here are the recommended actions:")
        engine.prioritized_actions.sort(reverse=True, key=lambda x: x[0])
        for priority, action in engine.prioritized_actions[:5]:
            st.write(f"**Priority {priority:.1f}:** {action}")
    else:
        st.warning("No critical actions were triggered. Consider revisiting the input values or further inspections.")

# Footer Section
st.markdown("---")
st.markdown(
    """
    <style>
    .footer {
        font-size: 14px;
        color: #7f8c8d;
        text-align: center;
        padding: 10px 0;
    }
    .footer a {
        color: #3498db;
        text-decoration: none;
        margin: 0 5px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <div class="footer">
        Developed by <b>Walid Alsafadi</b><br>
        <a href="https://github.com/WalidAlsafadi" target="_blank">GitHub</a> |
        <a href="https://linkedin.com/in/WalidAlsafadi" target="_blank">LinkedIn</a> |
        <a href="https://twitter.com/WalidAlsafadi" target="_blank">Twitter</a>
    </div>
    """, unsafe_allow_html=True
)