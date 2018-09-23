# Outlook Auto-Grouper

## Quickstart

### Prereq Installations

* Docker

* Docker-Compose

### Getting Started

1. Get list of emails

    Generally speaking, the list of emails will come from the member spreadsheet.

2. Paste list of emails in python script

    When selecting the row of all emails, pasting will results in a newline delimited list. You will paste that list in ```AutoGrouper.py``` in the multiline string which is then split and assigned to the GROUPIES var.

    This:

    ```python
    GROUPIES = """""".split("\n")
    ```

    Should turn into this:

    ```python
    # Newline delimited list of emails
    GROUPIES = """example@example.com
    example@example.com
    example@example.com""".split("\n")
    ```

3. Provide Credentials, and Name Group

    You will input your outlook creds into the following variables:

    ```python
    # Email Username (literally the email)
    USERNAME = ""

    # Password
    PASSWORD = ""
    ```

    You will then input the desired Group Name into this variable:
    ```python
    # What you want the group to be named
    GROUP_NAME = ""
    ```

4. Build the Python container

    The Python container will always need to be rebuilt if any changes are made to any of the files inside of the ```Python/``` directory; keep that in mind. We just made some changes, and though the container will be built on the first run anyway, it's healthy to get in this habit so that you don't forget later.

    ```bash
    ~/AutoGrouper $ docker-compose build
    ```

5. Run the container

    Don't forget, if you made any changes to any of the files inside of the ```Python/``` directory, you will need to rebuild the container with ```docker-compose build``` like in step 4. Assuming that you successfully completed step 4, you will need to run:

    ```bash
    ~/AutoGrouper $ docker-compose up
    ```

    If everything goes accordingly, you should see this output:

    ```bash
    Finished Making "GROUP NAME YOU PUT IN THE PYTHON SCRIPT" Email List
    ```

    and then this somewhere after:

    ```bash
    compclubgrouper_python_1 exited with code 0
    ```

    Then, CTRL+C to kill docker-compose, and run the following to perform cleanup on the residual containers:

    ```bash
    ~/AutoGrouper $ docker-compose down
    ```

6. That's all folks

    If you have any trouble, reread the steps, then shoot an email to riley.johnson@trojans.dsu.edu or message Riley Johnson on slack; then email rj@therileyjohnson.com if you don't hear a response from either of those