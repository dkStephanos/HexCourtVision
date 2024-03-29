![image](https://github.com/dkStephanos/HexCourtVision/blob/master/backend/static/app/content/readme.webp)

# HexCourtVision

**HexCourtVision** is an advanced analytics platform aimed at transforming NBA game data into actionable insights, specifically focusing on Dribble Hand-Off (DHO) actions.

## Project Structure
- `backend/`: Django REST framework-based backend.
- `frontend/`: Future user interface for interaction (under development).
- `ml_nba/`: Machine learning, data preprocessing, and visualization modules.
- `notebooks/`: Jupyter notebooks for data analysis and model execution.

## Installation

```bash
git clone https://github.com/dkStephanos/HexCourtVision
cd HexCourtVision
docker-compose up
```

## Preprocessing
Transform raw game data into a structured format.

```python
from ml_nba.preprocessing.process_game import process_game
game_df = process_game("20151228SACGSW")
```

## Candidate Extraction
Identify potential DHO actions.

```python
from ml_nba.preprocessing.extract_dho_candidates import extract_dho_candidates
dho_candidates = extract_dho_candidates("20151228SACGSW")
```

## Hexmap Generation
Generate hexmaps to represent player movements.

```python
# Placeholder for hexmap generation code
hexmap = generate_trajectory_image(target_event, target_candidate)
```

![image](https://github.com/dkStephanos/HexCourtVision/blob/master/backend/static/app/content/hexmap.png)

## Classification
Train and evaluate an SVM classifier.

```python
from ml_nba.classification.train_and_evaluate import train_and_evaluate_svm
results = train_and_evaluate_svm(C=0.75, kernel='poly', test_size=0.3, shuffle=True, n_iterations=None)
```

## Clustering
Analyse player movements and game patterns.

```python
from ml_nba.clustering.run_clustering import run
run(n_clusters = 8
    hex_dir = 'C:\\Users\\Stephanos\\Documents\\Dev\\NBAThesis\\NBA_Thesis\\static\\backend\\hexmaps'
    directory = os.fsencode(hex_dir)
    image_names = []
    images = []
    hexmaps = [])
```

## Contributing
Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

## License
This project is licensed under the MIT License - see LICENSE.md for details.
