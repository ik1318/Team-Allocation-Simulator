# Team Allocation Simulator

*Developed as part of a group project for SC1003.*

The Team Allocation Simulator is a data-driven tool designed to automate the complex task of forming student project teams. In large educational settings, manually sorting students to ensure fair and diverse teams is time-consuming and prone to bias. 

THIS PROJECT PERFORMS THE FOLLOWING JOBS:
- Data Processing: Cleansing and structuring messy student records (Tutorial Group, School, Gender, CGPA).
- Algorithmic Sorting: Automating the assignment of students to teams based on academic, gender, and school diversities.
- Performance Verifying: Providing visual proof (charts and trends) that shows how the algorithm outperforms standard random sorting.
- Result Exporting: Producing a ready-to-use CSV file with assigned team numbers for immediate administrative use.

CORE FEATURES
- Intelligent Grouping: Uses a greedy optimization algorithm to assign students to teams based on fitness scores.
- Diversity-Aware Optimization:
  - Academic Balance: Ensures groups have a comparable CGPA distribution, preventing the clustering of high or low performers.
  - Gender Diversity: Balances male and female participation across groups.
  - School Mix: Prevents large clusters from the same school (e.g., School of Computer Science) in a single group.
- Comprehensive Reporting: Generates visual performance summaries and optimization trends (Group Sizes 4-49).
- Result Export: Automatically generates data/grouped_records.csv with final assignments.

PROJECT STRUCTURE
- main.py: Entry point for running the simulator.
- src/: Core logic and analysis modules.
- data/: Input (records.csv) and Output (grouped_records.csv).
- outputs/: Generated performance visualizations (.png).
- docs/: Project requirements and supplementary documents.

HOW IT WORKS
1. Data Ingestion: Loads and cleans student records from data/records.csv, removing group prefixes and converting types.
2. Scoring Engine: Evaluates every potential student-to-group assignment using a fitness function (grade) that quantifies the diversity impact of adding a specific student.
3. Optimized Sorting: Iteratively assigns students to the group that yields the highest fitness score until all teams are filled.
4. Validation: Compares the algorithmic result against a randomized control to calculate percentage improvements in balance and diversity.

TECH STACK
- Language: Python 3.x
- Data Engineering: Pandas (Preprocessing & Cleansing)
- Mathematical Logic: Statistics & Math modules (Scoring & Fitness)
- Visualization: Matplotlib & Seaborn (Performance Graphing)
- Packaging: Modular directory structure for scalability.
