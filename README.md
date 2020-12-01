
# A23_NFL_Big_Data_Bowl
Link to Kaggle Competition: [Big Data Bowl](https://www.kaggle.com/c/nfl-big-data-bowl-2021).
“When a quarterback takes a snap and drops back to pass, what happens next may seem like chaos. As offensive players move in various patterns, the defense works together to prevent successful pass completions and then to quickly tackle receivers that do catch the ball.” 

## Data Files
Due to the large amount of data, you can view all the datasets and generated images 
[here](https://drive.google.com/drive/folders/1nwsG9g1qVgHOhs6BSZzKYKVy5b6Ff8e_?usp=sharing).

## Code Files

**Image Generation Logic :** //image-generation//main.py
Takes the data from the provided datasets(plays.csv and week csv's) and creates images that represent player positions on a football field. Saves the data labels alongside the image name. 

**Deep Learning Model:** NFLNeuralNetwork.ipynb
Classifies images using a CNN   
