import streamlit as st
from building_assessment_ES import BuildingAssessment, BuildingAssessmentExpertSystem

# Title and Project Information
st.markdown("<h1 style='text-align: center; color: dodgerblue;'>Expert System for Gaza Post-War Building Assessment</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Designed by Walid Alsafadi</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>University College of Applied Science</h5>", unsafe_allow_html=True)
st.divider()

# Section: Structural Assessment
st.header("Structural Assessment")
st.caption("Evaluate structural conditions such as cracks and damage.")
sar_backscatter = st.checkbox(
    "Is severe SAR backscatter detected (indicating structural damage)?",
    help="Select this if remote sensing (SAR) indicates significant structural deformation."
)
has_cracks = st.checkbox(
    "Does the building have cracks?",
    help="Select this if there are visible cracks in the building's structure."
)
if has_cracks:
    cracks = st.selectbox(
        "Type of cracks:",
        ["minor", "moderate", "severe"],
        help="Classify the cracks based on their severity."
    )
    load_bearing_cracks = st.checkbox(
        "Are there cracks in load-bearing walls?",
        help="Select this if critical structural cracks are present in load-bearing walls."
    )
    crack_width = st.slider(
        "Width of cracks (mm):",
        1.0, 50.0, 1.0,
        help="Specify the measured width of the cracks in millimeters."
    )
    cracks_worsening = st.checkbox(
        "Are the cracks worsening over time?",
        help="Select this if minor cracks are worsening over time."
    )
else:
    cracks = "none"
    load_bearing_cracks = False
    crack_width = 0.0
    cracks_worsening = False

st.divider()

# Section: Environmental Factors
st.header("Environmental Factors")
st.caption("Consider environmental risks such as hazardous zones and radiation.")
hazardous_zone = st.checkbox(
    "Is the building in a hazardous zone?",
    help="Select this if the building is located in an area with environmental risks (e.g., flooding, radiation)."
)
if hazardous_zone:
    radiation_level = st.slider(
        "Radiation Level (mSv/year):",
        1.0, 5.0, 1.0,
        help="Specify the measured radiation level. Minimum hazardous level is 1.0 mSv/year."
    )
else:
    radiation_level = 0.0
unexploded_ordnance = st.checkbox(
    "Are there minefields/unexploded ordnance nearby?",
    help="Select this if the area is contaminated with minefields or unexploded ordnance."
)
contaminated_materials = st.checkbox(
    "Are contaminated materials detected?",
    help="Select this if the building materials are contaminated and unsafe."
)

st.divider()

# Section: Data and Utility Analysis
st.header("Data and Utility Analysis")
st.caption("Analyze utility damage, accessibility, and data inconsistencies for informed decisions.")
significant_difference = st.checkbox(
    "Significant differences in damage assessments?",
    help="Select this if multiple damage assessments significantly differ."
)
conflicting_data = st.checkbox(
    "Are there conflicting SAR and optical data?",
    help="Select this if remote sensing data (SAR vs. optical) shows conflicting results."
)
missing_records = st.checkbox(
    "Are pre- and post-war property records missing?",
    help="Select this if historical records are unavailable."
)
damaged_utilities = st.checkbox(
    "Are there damaged sewer or water pipes?",
    help="Select this if the building's utilities (e.g., sewer, water pipes) are damaged."
)
access_to_power = st.checkbox(
    "Does the building have access to power?",
    help="Select this if the building has reliable access to power."
)
road_inaccessibility = st.checkbox(
    "Are roads to the building inaccessible?",
    help="Select this if road access to the building is blocked or damaged."
)

st.divider()

# Section: Social and Infrastructure Assessment
st.header("Social and Infrastructure Assessment")
st.caption("Assess social impact, overcrowding, and proximity to critical infrastructure.")
overcrowding = st.checkbox(
    "Is the building overcrowded?",
    help="Select this if the building is overcrowded beyond its capacity."
)
vulnerable_population = st.checkbox(
    "Does the building house vulnerable groups?",
    help="Select this if the building houses vulnerable populations (e.g., elderly, children)."
)
critical_infrastructure = st.checkbox(
    "Is the building near critical infrastructure?",
    help="Select this if the building is close to critical infrastructure like hospitals or schools."
)
hospitals_or_schools = st.checkbox(
    "Is the building near hospitals or schools?",
    help="Select this if the building is close to hospitals or educational institutions."
)
population_displacement = st.checkbox(
    "Does the population displacement exceed housing capacity?",
    help="Select this if the displaced population exceeds available permanent housing."
)
multiple_families = st.checkbox(
    "Does the building serve multiple families?",
    help="Select this if the building serves as a residence for multiple families."
)
income_below_poverty = st.checkbox(
    "Is the income level below the poverty threshold?",
    help="Select this if the income level of residents is below the poverty threshold."
)

st.divider()

# Section: Design and Sustainability Considerations
st.header("Design and Sustainability Considerations")
st.caption("Explore the feasibility of modern design standards and renewable energy integration.")
outdated_design = st.checkbox(
    "Does the building design predate modern codes?",
    help="Select this if the building was designed before modern construction standards."
)
renewable_energy_possible = st.checkbox(
    "Is renewable energy integration feasible?",
    help="Select this if the building can integrate renewable energy systems."
)
temporary_shelter_needed = st.checkbox(
    "Are displaced residents requiring temporary housing?",
    help="Select this if the displaced residents require immediate temporary housing."
)

st.divider()

# Run the Expert System
if st.button("Run Expert System"):
    # Initialize the expert system
    engine = BuildingAssessmentExpertSystem()
    engine.reset()

    # Declare facts based on user inputs
    engine.declare(
        BuildingAssessment(
            sar_backscatter=sar_backscatter,
            cracks=cracks,
            load_bearing_cracks=load_bearing_cracks,
            crack_width=crack_width,
            cracks_worsening=cracks_worsening,
            hazardous_zone=hazardous_zone,
            radiation_level=radiation_level,
            unexploded_ordnance=unexploded_ordnance,
            contaminated_materials=contaminated_materials,
            significant_difference=significant_difference,
            conflicting_data=conflicting_data,
            missing_records=missing_records,
            damaged_utilities=damaged_utilities,
            access_to_power=access_to_power,
            road_inaccessibility=road_inaccessibility,
            overcrowding=overcrowding,
            vulnerable_population=vulnerable_population,
            critical_infrastructure=critical_infrastructure,
            hospitals_or_schools=hospitals_or_schools,
            population_displacement=population_displacement,
            multiple_families=multiple_families,
            income_below_poverty=income_below_poverty,
            outdated_design=outdated_design,
            renewable_energy_possible=renewable_energy_possible,
            temporary_shelter_needed=temporary_shelter_needed,
        )
    )
    engine.run()

    # Display results
    st.subheader("Results")
    if engine.prioritized_actions:
        st.success("Analysis complete. Here are the recommended actions:")
        st.write("**Top Actions (Prioritized):**")
        engine.prioritized_actions.sort(reverse=True, key=lambda x: x[0])  # Sort by priority
        for priority, action in engine.prioritized_actions[:5]:  # Limit to top 5
            st.write(f"**Priority {priority:.1f}:** {action}")
    else:
        st.error("No actions were triggered based on the inputs.")

st.divider()

# Footer
st.markdown("<p style='text-align: center; color: gray;'>Developed by <b>Walid Alsafadi</b> © 2025</p>", unsafe_allow_html=True)