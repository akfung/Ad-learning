# Ad-learning

Since the 2016 election, the relevance and impact of social media advertising on politics has become
more obvious to the public. This website was created in an effort to analyze the features of political ads on Facebook's 
social media platforms as made available through their Ad Library API.

Data gathered using the response library in Python and added to PostgreSQL database using Pandas, psycopg2, and Flask-SQLAlchemy. Database querries and API endpoint handled by Flask. Ad text classified by a Tensorflow keras recurrent neural network with LSTM layer trained on the imdb_reviews/plain_text dataset and civil_comments dataset. Visualizations prepared with Plotly.js and amCharts4, while the html was built with bootstrap. Web application hosted on Heroku with Postgres addon.
