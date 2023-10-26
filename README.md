# Dataminers

# Members
Zizheng  Zhang (Sean)

Tel: 301-742-4626

Bio:
- Bachelor of Arts, Beijing University of Chemical Technology (Beijing, 2014-2019)
- Junior Software Developer (C#, Unity, and Web full-stack), JHBY Tech Co. Ltd. (Beijing, 2019-2022)
- Master of Science, University of Maryland, College Park (College Park, 2022-2023)

Yinming Gao (Randall)

Tel: 240-413-2158

Bio：
- Bachelor of Science, Shandong University of Science and Technology （Shandong, 2017-2021）
- Data Analyst Intern, DataStory （Beijing, 2021-2022）
- Master of Science, University of Maryland, College Park （College Park, 2022-2023）

# Abstract - Analysis of Head Start Accessibility across the Continental U.S.
Established in 1965, Head Start promotes school readiness for children in low-income families by offering educational, nutritional, health, social, and other services. The program is rooted in urban, suburban, and rural communities throughout the nation.

To better facilitate the course of Head Start, we analyzed public data to estimate the accessibility of the Head Start program in the continental United States. We constructed multiple metrics to measure and compare the accessibility of Head Start across the states and counties. The areas where communities might be underserved are identified by our metrics. Our analysis will help policy makers and federal agents to facilitate equal access to Head Start.

# Technologies In-use
Python: for data extraction, data analysis, and statistical modeling.

Tableau: for data visualization.

PowerPoint: for the presentation of insights.

# List of Python Libraries
Please see the file `requirements.txt` for a comprehensive list of all the used Python libraries in this project.
For successful execution of our notebook, please run the command `pip install -r requirements.txt` in the project directory. The command will automatically install all the Python libraries dependencies. The command requires the installation of PIP, a widely used Python package manager.


# Sample Visualizations
<img src='sample_visualization/unnamed.png'>
<img src='sample_visualization/unnamed (1).png'>
<img src='sample_visualization/unnamed (2).png'>
<img src='sample_visualization/unnamed (3).png'>

# Major Findings
We found that there are clusters of counties in both Texas and Georgia where the metric children per center have abnormally high values, indicating potential scarcity of Head Start recourse in those areas. Policy makers may need to find more Head Start participants in those areas so as to facilitate the accessibility of Head Start.

Nevada, Idaho, Arizona, Georgia, and Texas are the states with the lowest estimated enrollment rate, meaning that the communities in these five states are very likely to be underserved. Policy makers may need to increase public exposure to Head Start, especially to low-income families, so that low-income families are aware of Head Start and begin enrolling in Head Start.

A linear regression model was built to better understand and evaluate the funding policy of Head Start. We achieved an adjusted $R^{2}$ score of 0.971, indicating very successful regression modeling. The model suggests a strong correlation between funding amount, enrollment amount, and regional personal income level, showing that the funding policy of Head Start is well tailored to the actual situation of each state.

# Major Achievements
### Data Analysis
To accurately measure the impact and current situation of Head Start, we constructed multiple useful metrics to support our argument. The metrics that we have constructed and used include:
- Children per Center
- Fund per Child
- Funding Index
- Enrollment Rate
- Center Coverage Rate

Each of the metrics is intended to solve one or a group of closely related questions. And they performed well both measuring the program impact and identifying potential inequality. We believe that our metrics can also inspire data analytics practitioners to build more precise and unbiased metrics in their own domain of work.

### Automated Analytics Pipeline
Apart from conduting data analysis on multiple public datasets, we also managed to develop an automated data analytics pipeline that fetches external datasets and transform them into format ready for visualization and finding insights.

#### Automated Datasets:
- SAIPE Dataset
- BEA Regional Economic Dataset
- Head Start Annual Fiscal Report Dataset
- Head Start Location Dataset

Our data pipeline provides the utility to extract the above listed datasets by year, and will work consistently in the future as long as the datasource keeps their current interfacing pattern. Our pipelining service is currently implemented in the form of a web server, which, with a set of very consice user interfaces, enables users to fetch data and download them in well formatted CSV format.

Our application also demonstrates the potential of automating data analytics pipeline, which helps practitioners to focus on the analytics tasks without having to write analysis irrelevant codes by themselves, thereby saving their time and better facilitate productivity.

For a preview of our automated data pipeline, please visit http://54.90.52.121/