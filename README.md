# Expert System for Gaza Post-War Building Assessment

[**🌐 Access the Deployed App**](https://building-assessment-es.streamlit.app/)

This project implements a rule-based expert system to assist engineers in assessing post-war building conditions in Gaza. The system evaluates various structural, environmental, social, and utility-related factors to prioritize actions for reconstruction, repair, or temporary solutions.

## Features
- **Rule-Based Inference:** Implements 50+ rules to assess building conditions based on predefined criteria.
- **Uncertainty Handling:** Confidence levels for rules like cracks and radiation ensure accurate prioritization.
- **Prioritization Mechanism:** Outputs are ranked by severity and relevance.
- **Professional UI:** A polished Streamlit-based web interface with logical grouping, collapsible sections, and integrated social links.
- **Robust Testing:** Includes tests for individual rules, combined scenarios, and edge cases, with all rules validated.
- **Future-Proof Design:** Modular structure enables easy updates and expansions.

## Project Structure
- **`src/`**: Contains the main expert system implementation.
  - `building_assessment_ES.py`: Contains the rule-based logic of the expert system.
  - `building_assessment_UI.py`: Implements the Streamlit-based user interface for easy input and results visualization.
- **`test/`**: Includes all test cases and the notebook for validation.
  - `testing.ipynb`: Jupyter Notebook for individual and combined rule testing.
- **`docs/`**: Project documentation and supporting files.
  - `Preliminary Report - Challenges of Post-War Building Assessment in Gaza.pdf`: Preliminary report.
  - `Building Assessment Expert System - Guidelines.pdf`: Project instructions.

## Dependencies

This project requires the following dependencies:
- **Streamlit:** For building the web-based user interface.
- **Custom Fork of Experta:** A modified version of the `experta` library to ensure compatibility with Python 3.10+. The fixed version replaces `frozendict` with `immutabledict` and is installed automatically via:
  ```plaintext
  git+https://github.com/WalidAlsafadi/experta.git
  ```

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/WalidAlsafadi/BuildingAssessment-ExpertSystem
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Usage
### Running the Expert System via the UI

1. Launch the Streamlit UI:
   ```bash
   streamlit run src/building_assessment_UI.py
   ```
2. Follow the interactive interface to input building conditions and view prioritized actions.

### Running the Expert System via Python

1. Import the system into your script:
   ```bash
   from src.building_assessment_ES import BuildingAssessment, BuildingAssessmentExpertSystem
   ```
2. Define input facts and run the engine:
   ```bash
   engine = BuildingAssessmentExpertSystem()
   engine.reset()
   engine.declare(BuildingAssessment(hazardous_zone=True, overcrowding=True))
   engine.run()
   engine.print_prioritized_actions()
   ```

## Testing
1. Open the Jupyter Notebook in the `test` folder:
   ```bash
   jupyter notebook test/testing.ipynb
   ```
2. Run individual and combined scenario tests.
3. Validate the outputs in the notebook.

## How It Works
- The expert system uses a rule-based inference engine with 38 predefined rules.
- Users input building conditions via the UI, which are converted into facts for the system to process.
- Based on the rules and priorities, the system provides actionable recommendations.

## Future Enhancements and Updates
As this expert system evolves, future improvements may include:

- **Expanded Rule Set:** Add more granular rules to cover additional factors, such as material composition and advanced structural dynamics.
- **Machine Learning Integration:** Incorporate machine learning to complement rule-based decisions with predictive analytics.
- **Mobile Accessibility:** Develop a mobile-friendly version of the UI for use in the field.
- **Dynamic Data Sources:** Integrate real-time data sources, such as satellite imagery or IoT sensors, for automated fact updates.
- **Multi-Language Support:** Offer the interface in Arabic and other languages to improve accessibility for local engineers.
- **Advanced Visualization:** Provide 3D visualizations of damaged structures to aid in assessment.

## Authors
- Walid Alsafadi

## License
This project is licensed under the Apache License. See `LICENSE` for details.

---

Let me know if there’s anything else you’d like to modify! 😊
