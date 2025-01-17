# Expert System for Gaza Post-War Building Assessment

[**🌐 Access the Deployed App**](https://building-assessment-es.streamlit.app/)

This project implements a **rule-based expert system** to assist engineers in assessing post-war building conditions in Gaza. The system evaluates various **structural, environmental, social, and utility-related factors** to prioritize actions for reconstruction, repair, or temporary solutions.

---

## Features
- **Rule-Based Inference**: Implements **40+ rules** to assess building conditions based on predefined criteria.
- **Uncertainty Handling**: Uses **fuzzy logic**, **confidence levels**, and **priority ranking** for accurate recommendations.
- **Prioritization Mechanism**: Outputs are ranked by severity and relevance.
- **Professional UI**: A polished **Streamlit-based web interface** with logical grouping, dynamic inputs, and integrated social links.
- **Robust Testing**: Includes tests for individual rules, combined scenarios, and edge cases, ensuring rule validation.
- **Successful Deployment**: Fully deployed and accessible online.

---

## Project Structure
- **`src/`**: Contains the main expert system implementation.
  - `building_assessment_ES.py`: Implements rule-based logic for building assessment.
  - `building_assessment_UI.py`: Streamlit-based user interface for user interaction and result visualization.
- **`test/`**: Includes test cases and a validation notebook.
  - `testing.ipynb`: Jupyter Notebook for individual and combined rule testing.
- **`docs/`**: Project documentation and supporting files.
  - `Final Report - A Rule-Based Expert System for Post-War Building Assessment in Gaza (2025).pdf`: Final report detailing the system and its development.
  - `Presentation - Rule-Based Expert System for Post-War Building Assessment in Gaza`: PowerPoint presentation summarizing the project.

---

## Dependencies

This project requires the following dependencies:
- **Streamlit**: For building the user interface.
- **NumPy**: Numerical computations.
- **SciPy**: Used by scikit-fuzzy for advanced computations.
- **Scikit-Fuzzy**: For fuzzy logic implementation.
- **Custom Fork of Experta**: A modified version of the `experta` library compatible with Python 3.10+. Install via:
  ```plaintext
  git+https://github.com/WalidAlsafadi/experta.git
  ```

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/WalidAlsafadi/BuildingAssessment-ExpertSystem
   ```

2. Navigate to the project directory:
   ```bash
   cd BuildingAssessment-ExpertSystem
   ```

3. Install the required dependencies:
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
- The system uses rule-based inference with 40+ predefined rules to assess building conditions.
- Users input building conditions through a user-friendly UI.
- The system processes these inputs and provides actionable recommendations based on priority and confidence.

## Future Enhancements and Updates
As this expert system evolves, future improvements may include:

- **Expanded Rule Base**: Adding new rules to address emerging challenges in post-conflict zones.
- **Machine Learning Integration**: Predict building damage or prioritize reconstruction based on historical data.
- **Enhanced User Experience**: Improving the UI for better usability and multi-language support.
- **Real-Time Data**: Integration of real-time data (e.g., satellite imagery) for more precise assessments.

## Authors
- Walid Alsafadi

## License
This project is licensed under the Apache License. See `LICENSE` for details.

---

Let me know if further refinements are needed! 😊