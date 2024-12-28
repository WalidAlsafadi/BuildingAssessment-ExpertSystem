# Building Assessment Expert System

This project implements a rule-based expert system to assist in post-war building assessments. The system evaluates various structural, environmental, social, and utility-related factors to prioritize actions for reconstruction, repair, or temporary solutions.

## Features
- **Rule-Based Inference:** 31 rules to assess building conditions.
- **Uncertainty Handling:** Confidence levels for rules like cracks and radiation.
- **Prioritization Mechanism:** Actions are prioritized based on predefined logic.
- **Robust Testing:** Includes individual rule tests, combined scenarios, and edge cases.

## Project Structure
- **`src/`**: Contains the main expert system implementation.
  - `building_assessment_es.py`: Core logic for the rule-based system.
- **`test/`**: Includes all test cases and the notebook for validation.
  - `testing.ipynb`: Jupyter Notebook for individual and combined rule testing.
- **`docs/`**: Project documentation (e.g., PDF report).
  - `Challenges of Post-War Building Assessment in Gaza and Rule-Based Solutions.pdf` Preliminary report.
  - `Expert Systems Final Project.pdf` Projects Instructions.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install experta
   ```
## Usage
## Running the Expert System

1. Import the system into your Python script:
   ```bash
   from src.building_assessment_es import BuildingAssessment, BuildingAssessmentExpertSystem
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
1. Open the Jupyter Notebook in the `testing/` folder:
   ```bash
   jupyter notebook testing/testing.ipynb
   ```
2. Run individual and combined scenario tests.
3. Validate the outputs in the notebook.

## Authors
- Walid Alsafadi

## License
This project is licensed under the Apache License. See `LICENSE` for details.

---

Would you like me to adjust anything else or help with the smaller README for the `testing/` folder? Let me know! 😊
