# COMP20008-Assignment-2
doyeong.kim@student.unimelb.edu.au  
shuyzhang2@student.unimelb.edu.au  
kunal.dewani@student.unimelb.edu.au  
## [Assignment Spec](https://canvas.lms.unimelb.edu.au/courses/183329/assignments/474202)

## How to run the program
Firstly, run `pip3 install -r requirements.txt` to install required packages.
Then, run `python3 main.py` to run the program. Follow the program prompts to generate output.  
To calculate the root mean squared error for the recommendation system, exit the program loop and select 'y' to generate the output.  
Optionally, run `python3 test_item_item_similarity.py` to calculate the RMSE directly.

## Sample inputs to the program
- Choose Option 1 from the main menu and search for User-ID 4809. This user's favourite book is *Harry Potter and the Chamber of Secrets*, and they are recommended five of the other *Harry Potter* books in the series.
- From the Main Menu, enter {3, 4, 1, 3499229412} to get recommendation based on ISBN. That ISBN is a German book titled *Meineid: Roman*, and the program recommends five other German books.
- From the Main Menu, enter {2, 1} or {2, 2} to get the highest rated and most popular authors, respectively.
- From the Main Menu, enter {3, 1} or {3, 2} to get the highest rated and most popular books, respectively.
- When searching for a specific author, book title, or ISBN, entering an incorrect input will find and return the closest match to the user input. For example, from the Main Menu, search for a specific author by entering {2, 3, Dr. Suss}. This will suggest the closest matched author, Dr. Seuss.

## Github Rules

### Main branch  
`main` represents the official project history.  
Instead of committing directly on their local `main` branch, developers create a new branch every time they start work on a new feature. Feature branches should have descriptive names, like animated-menu-items or issue-#1061. The idea is to give a clear, highly-focused purpose to each branch

### Git Feature Branch Workflow
Please follow the [**Git feature branch workflow**](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow). The core idea behind the Feature Branch Workflow is that all feature development should take place in a dedicated branch instead of the main branch. 

## Helper Functions
Scripts containing helper functions are included in the `helpers` directory.

### List of Helper Scripts
* file_io
    * Contains helper functions to ingest the csv data from the data directory
* data_processing
    * Contains functions related to processing data in Pandas DataFrames

### How to use Helper Functions
To use helper functions, import the specific functions you'd like to use from the helper script located in the `helpers` directory.  

**Example:**  
`from helpers.file_io import ingest_books`  
**Use:**  
`df = ingest_books()`

### How to add new helper functions
To add new helper functions, simply add the function definition to the relevant helpers file. If no relevant file exists, make a new file and add the functions there.



