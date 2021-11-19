import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from boto.s3.connection import S3Connection
 
PORT = int(os.environ.get('PORT', 5000))



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.environ.get('TOKEN')

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    check()

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://dhonmaniks.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

def check():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    import info

    # make sure this path is correct
    PATH = os.environ.get("CHROMEDRIVER_PATH")

    driver = webdriver.Chrome(PATH)

    RTX3070LINK1 = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442&intl=nosplash"
    RTX3070LINK2 = "https://www.bestbuy.com/site/gigabyte-geforce-rtx-3070-8g-gddr6-pci-express-4-0-graphics-card-black/6437912.p?skuId=6437912&intl=nosplash"
    XBOXONETEST = "https://www.bestbuy.com/site/microsoft-xbox-one-s-1tb-console-bundle-white/6415222.p?skuId=6415222&intl=nosplash"

    driver.get(RTX3070LINK1)

    isComplete = False

    while not isComplete:
        # find add to cart button
        try:
            atcBtn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button"))
            )
        except:
            driver.refresh()
            continue

        print("Add to cart button found")
        update.message.reply_text('doing this!')


        try:
            # add to cart
            atcBtn.click()

            # go to cart and begin checkout as guest
            driver.get("https://www.bestbuy.com/cart")

            checkoutBtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[2]/div[1]/div/div/span/div/div[2]/div[1]/section[2]/div/div/div[3]/div/div[1]/button"))
            )
            checkoutBtn.click()
            print("Successfully added to cart - beginning check out")

            # fill in email and password
            emailField = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "fld-e"))
            )
            emailField.send_keys(info.email)

            pwField = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "fld-p1"))
            )
            pwField.send_keys(info.password)

            # click sign in button
            signInBtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/section/main/div[1]/div/div/div/div/form/div[3]/button"))
            )
            signInBtn.click()
            print("Signing in")

            # fill in card cvv
            cvvField = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "credit-card-cvv"))
            )
            cvvField.send_keys(info.cvv)
            print("Attempting to place order")

            # place order
            placeOrderBtn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".button__fast-track"))
            )
            placeOrderBtn.click()

            isComplete = True
        except:
            # make sure this link is the same as the link passed to driver.get() before looping
            driver.get(RTX3070LINK1)
            print("Error - restarting bot")
            continue

    print("Order successfully placed")


if __name__ == '__main__':
    main()