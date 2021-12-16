#ASSETS FOLDER DEFINITION 

**Assets folder is expected to contain the following files:**
> influencers.csv 
> telegram-history.csv 
> trend-items.csv 
> items-record.csv 
> telegram-data.json 
> media-output.json 
> recognition-output.json 
> retail-output.json
> instaImages folder 

**Description of the file management:**
The following files will never be deleted, information will be added to them once per week. 
> influencers.csv 
> telegram-history.csv 
> items-record.csv

The following files / directories will be deleted and rewritten once per week 
> trend-items.csv 
> telegram-data.json 
> media-output.json 
> recognition-output.json 
> retail-output.json
> instaImages folder 

**Description of the file content:**
> influencers.csv 
Contains a 3-column csv. Columns are: 'username', 'gender', 'score'.
Contains the username of the influencers whose pictures are downloaded in InstaImages folder. Their gender, and their associated trend-generation score [0-1]. Initially, all scores are set to 0.5. 

> telegram-history.csv
Contains a 6 column csv. Columns are: 'item', 'gender', 'yes_votes', 'no_votes', 'total_votes', 'average_yes_proportion'. 
File is filled by rows, it documentates the results of the surveys of the Telegram blog. It is filled by rows.
Average_yes_proportion stores the average_yes_proportion of the telegram blog up to the last survey, not the average_yes_proportion of only the last survey. Analysis of this file serves to edit influencer score, stores in influencers.csv .

> trend-items.csv 
Contains a 3 column csv. Columns are: prenda, gender, influencers. 
It contains the items that have been predicted as trend for the week. 

> items-record.csv 
Contains a 3 column csv. Columns are: 'item', 'gender', 'influencers'
Contains the items predicted as trend and the percentage of appereance on their week and the following weeks. It serves to monitor if the predicted trend has become trendy. Analysis of this file serves to edit influencer score, stores in influencers.csv .

> telegram-data.json 
Contains the results of 1 survey corresponding to a post posted on the telegram blog. Data stored here is passed to telegram-history.csv . 

> media-output.json 
Contains the information of all images contained in instaImages folder. Meaning the following parameters are described for each image: "likes", "date", "imageSrc", "followers", "user", "gender". 

> recognition-output.json 
Contains the information stored in media-output.json + the clothing items and their color, per image, recognized in Image Recognition. 

> retail-output.json
Contains the information of the clothing items selected from retail stores. 

> instaImages folder 
Contains the images downloaded from instagram that will be feeded to the system, whith which trends will be predicted. 
