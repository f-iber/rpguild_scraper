A program that will take the text of posts on the guild and save them into a spreadsheet. This can be used for preservation, for large scale studies, or whatever else you find amusing. Please be judicious when using it.

# To install:
Unzip the folder somewhere

Make sure python is installed on your computer. These guides can help
https://docs.python.org/3/using/windows.html
https://docs.python.org/3/using/mac.html
https://docs.python.org/3/using/unix.html

(Ensure that the "Add Python to PATH" option is selected when installing on Windows)


Make sure you have all the packages listed in requirements.txt, you can run the following command on the command line to check:

pip install -r requirements.txt

The above command should be run in whatever directory you placed requirements.txt in



# Usage:

List all the threads you want to scrape in the threads.csv file.

In the first column, either list the full url of the thread or the number that functions as the thread ID. 
Thread ID can be in the url, it's highlighted here
https://www.roleplayerguild.com/topics/**182217**-ask-an-admin-v2/ooc?page=10#post-5142195

If you list the thread ID, the program will fill in the rest of the URL for you while it scrapes

If you want to specify a range using thread IDs, list the first ID at in the first column and the second ID in the second column. It will collect those threads and every one between them. For example, 530 in column 1 and 534 in column 2 would collect the threads with IDs of 530, 531, 532, 533 and 534

threads.csv is a spreadsheet, it can be edited with Excel, LibreOffice calc, Google Sheets, a text editor, or any similar program

Once you have all of threads you are intend to collect run the program.

While in the directory, you can run the script from the commandline, like this:

python guild\_scrape_script.py

If you're not comfortable running from the commandline, there's a simple script that will do it for you, using none of the options.


Click on the respective version of just_run for your operating system to run it. 

If you want to learn the command line to use the other options, you can use a tutorial like this:
https://tutorial.djangogirls.org/en/intro_to_command_line/

# Options:

    guild_scrape_script.py [--resume {True|False}] [--save {True|False}] [--limit number_goes_here] [--HTML {True|False}]

An example is below:
    guild_scrape_script.py --resume False --save True --limit 10

Options are listed after the script name in the command line

Everything contained in square brackets is optional, if not specified it will default to False. Limit will default to zero.

## Available Options:
Save: If true, the script will save continuously and use in\_progress.csv to mark progress as it goes. This will slow it down, but preserve work in the case of an interruption.
After generating in_progress.csv, you can use resume from it later.

Resume: If True, will read from in_progress.csv instead of threads.csv to find threads to scrape. Use this to continue a process you started before, such as one stopped by a limit or saved midway through.

Limit: An integer. If it's greater than zero, the scraper will stop after scraping that many threads, limiting the total number of threads scraped. If paired with the save option it can be used to break a large job up into several smaller portions.

HTML: If True, will retrieve the raw HTML of a post instead of the text. Less readable, but more likely to preserve formatting if needed



# Output notes

All scraped posts are saved in posts.csv

If there are already posts in it, they will be appended to the end.

By default, the CSV file with the following headings:

**title**: Title of the thread

**forum**: Forum thread was found in. Includes the 
rest of the forum hierarchy

**page_count**: Number of pages in the thread

**GM**: GM, including any Co-GMs. For non-roleplay threads this will be the thread creator

**page**: Which section it was in, IC, OOC, or Char. 
Non-roleplay threads will always be OOC

**id**: Unique ID of the post, for future reference

**user**: User who made post

**date**: Timestamp on post.

**text**: Text of the post. By default it includes no tags, just text, including text in hiders

The CSV is encoded in UTF-8, make sure you open it in that mode if you want to see all of the lovely weirdness of the guild
Linebreaks are left in, stripping them may make it more readable.

# Known Issues

Weird stuff might happen if you give a thread ID belonging to a nonexistent or deleted thread

Coming Later (maybe):

Some actual tests

An ability to control how fast it retrieves pages (currently every .59 seconds)

A GUI?


