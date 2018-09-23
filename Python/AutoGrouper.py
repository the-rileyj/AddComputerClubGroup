import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from urllib3 import exceptions


# Email Username (literally the email)
USERNAME = ""

# Password
PASSWORD = ""

# What you want the group to be named
GROUP_NAME = ""

# Newline delimited list of emails
GROUPIES = """example@example.com
example@example.com
example@example.com""".split("\n")

def main():
    # Handles waiting for selenium container to boot up
    KICKSTART = True
    TRIES = 0

    while KICKSTART:
        try:
            with webdriver.Remote(command_executor="http://selenium-service:4444/wd/hub", desired_capabilities=DesiredCapabilities.FIREFOX) as firefox:
                print("Successfully Started", flush=True)
                KICKSTART = False

                # Create a 30 second driver wait, used later to wait for elements up to 30 seconds
                wait30 = ui.WebDriverWait(firefox, 30)

                # Navigate to MyDSU to get to webmail
                firefox.get("https://mydsu.dsu.edu/")

                # Wait until the link to webmail has loaded, then navigate to the webmail site
                wait30.until(lambda driver: driver.find_element_by_xpath(r"""//a[translate(text(), "W", "w")="webmail"]""") is not None)
                firefox.get(firefox.find_element_by_xpath(r"""//a[translate(text(), "W", "w")="webmail"]""").get_attribute("href"))

                # Wait until the webmail login has loaded, then log in
                wait30.until(lambda driver: driver.find_element_by_xpath(r"""//input[@name="username"]""") is not None)
                firefox.find_element_by_xpath(r"""//input[@name="username"]""").send_keys(USERNAME)
                firefox.find_element_by_xpath(r"""//input[@name="password"]""").send_keys(PASSWORD)
                firefox.find_element_by_xpath(r"""//span[text()="sign in"]""").click()

                # Wait until the webmail landing page has loaded, then navigate to the "People" section
                wait30.until(lambda driver: driver.find_element_by_xpath(r"""//button/*[text()="People"]""") is not None)
                firefox.find_element_by_xpath(r"""//button/*[text()="People"]""").click()

                # Wait until the "People" section has loaded, then start making a new group
                wait30.until(lambda driver: driver.find_element_by_xpath(r"""//button/*[text()="New"]""") is not None)
                firefox.find_element_by_xpath(r"""//button/*[text()="New"]""").click()

                # Wait for the create group model to pop up and click the "Create group" button
                wait30.until(lambda driver: driver.find_element_by_xpath(r"""//button/*[text()="Create group"]""") is not None)
                firefox.find_element_by_xpath(r"""//button/*[text()="Create group"]""").click()

                # Wait for the "Group form" to load, then fill in the form
                wait30.until(lambda driver: driver.find_element_by_xpath(r"""//input[@aria-label="Group name:"]""") is not None)
                # Fill in the group name
                firefox.find_element_by_xpath(r"""//input[@aria-label="Group name:"]""").send_keys(GROUP_NAME)

                # Find the input for adding members
                member_input = firefox.find_element_by_xpath(r"""//form/input""")

                # Start adding people to the group
                for number, GROUPIE in enumerate(GROUPIES):
                    # Clear the input just in case the last member was not correctly added
                    member_input.clear()
                    # Fill the input with the persons email
                    member_input.send_keys(GROUPIE)

                    # Wait for the typing to register so we can hit enter to add the email
                    sleep(.1)

                    # Hit enter on the input to add the email
                    member_input.send_keys(Keys.ENTER)

                    # Give update and wait briefly
                    print("{0:4.2f}% Complete  ".format(((number + 1) / len(GROUPIES)) * 100), flush=True)
                    sleep(.1)

                # Save the created group
                firefox.find_element_by_xpath(r"""//span[text()="SAVE"]""").click()

                # Wait until the group has been successfully created, then give an update
                wait30.until(lambda driver: driver.find_element_by_xpath(r"""//div/span[text()="{}"]""".format(GROUP_NAME)) is not None)
                print("\r\nFinished Making \"{}\" Email List\n".format(GROUP_NAME), flush=True)

        except exceptions.MaxRetryError:
            # Exception occurs when the webdriver cannot be connected to, will try 10 times
            if TRIES >= 10:
                print("Number of tries to connect to the web driver exceeded, try again.", flush=True)
                return
            print("Could not connect to webdriver, trying again.", flush=True)
            TRIES += 1
        except Exception as e:
            print("Unexpected exception occured, quiting out:\n{}".format(e), flush=True)
            return


if __name__ == "__main__":
    main()