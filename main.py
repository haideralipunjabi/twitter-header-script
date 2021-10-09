import os
import io
import requests
import tweepy
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Load environment variables from .env file
load_dotenv()

# Location of this file
parent_directory = os.path.dirname(os.path.abspath(__file__))

# Colors to be used in the header
COLORS = {
    "FOREGROUND": "#000000",
    "BACKGROUND": "#FFFFFF",
}

# Fonts to be used in the header
FONTS = {
    "TITLE": ImageFont.truetype(os.path.join(parent_directory, "fonts/SourceCodePro-Regular.ttf"), 48),
    "SUBTITLE": ImageFont.truetype(os.path.join(parent_directory, "fonts/SourceCodePro-Regular.ttf"), 30),
    "NUMBERS": ImageFont.truetype(os.path.join(parent_directory, "fonts/SourceCodePro-Regular.ttf"),  144),
    "FOOTER": ImageFont.truetype(os.path.join(parent_directory, "fonts/SourceCodePro-Regular.ttf"),  24),
}

# ID of the Tweet to be used
PINNED_TWEET_ID = "1435219303465324548"


# Authenticate to Twitter and return the API object
def get_twitter_api():
    auth = tweepy.OAuthHandler(
        os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
    auth.set_access_token(
        os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
    return tweepy.API(auth)

# Fetch the status and followers data
def get_status_data(api, status_id):
    status = api.get_status(id=status_id)
    followers = api.get_followers(
        count=3, skip_status=True)    # 3 Latest Followers
    return {
        "likes": status.favorite_count,
        "retweets": status.retweet_count,
        "followers": [{
            "username": follower.screen_name,
            "photo": follower.profile_image_url_https
        } for follower in followers]        # The username and profile picture only
    }

# Draw the Header
def draw_header(data):
    # Create a new Image 1500 x 500 with background color
    img = Image.new('RGB', (1500, 500), color=COLORS['BACKGROUND'])
    d = ImageDraw.Draw(img)  # Draw variable for drawing on the image
    # The rectangle which contains the test "My pinned tweet has"
    d.rectangle((30, 30, 680, 110), None, COLORS["FOREGROUND"], 5)
    # Text - My Pinned Tweet has
    d.text((355, 70), "My pinned tweet has",
           fill=COLORS["FOREGROUND"], font=FONTS["TITLE"], anchor="mm")

    # Likes and Likes Count
    d.text((500, 370), "LIKES",
           fill=COLORS["FOREGROUND"], font=FONTS["TITLE"], anchor="mm")
    d.text((500, 250), str(data["likes"]),
           fill=COLORS["FOREGROUND"], font=FONTS["NUMBERS"], anchor="mm")
    # Retweets and Retweets Count
    d.text((1000, 370), "RETWEETS",
           fill=COLORS["FOREGROUND"], font=FONTS["TITLE"], anchor="mm")
    d.text((1000, 250), str(data["retweets"]),
           fill=COLORS["FOREGROUND"], font=FONTS["NUMBERS"], anchor="mm")

    # Text - Latest Followers
    d.text((1300, 50), "Latest Followers",
           fill=COLORS["FOREGROUND"], font=FONTS["SUBTITLE"], anchor="mm")

    # Keeping track of widest line of text
    max_width = d.textsize("Latest Followers", font=FONTS["SUBTITLE"])[0]

    # Drawing the followers text and image
    for idx, follower in enumerate(data["followers"]):
        username_width = d.textsize(
            follower["username"], font=FONTS["SUBTITLE"])[0]
        if username_width + 50 > max_width:
            # 50 = Width of image (30) + gap between image and text (20)
            max_width = username_width + 50
        d.text((1320, 90 + 40*idx), follower["username"],
               fill=COLORS["FOREGROUND"], font=FONTS["SUBTITLE"], anchor="mm")
        # Download image
        profile_image = Image.open(io.BytesIO(
            requests.get(follower["photo"]).content))
        # Resize image
        profile_image = profile_image.resize((30, 30))
        # Paste Image
        img.paste(profile_image, (1280 - (username_width//2), 75 + 40*idx))

    # Draw rectangle around followers
    d.rectangle((1300 - (max_width/2) - 20, 30, 1300 +
                (max_width/2) + 20, 210), None, COLORS["FOREGROUND"], 5)

    # Footer Text
    d.multiline_text((750, 465), "Like / Retweet my pinned tweet to see my header update\nCheck pinned thread for more details",
                     fill=COLORS["FOREGROUND"], font=FONTS["FOOTER"], align="center", anchor="ms")
    # Save the image
    img.save(os.path.join(parent_directory, "header.png"))


# Driver Code
if __name__ == "__main__":
    api = get_twitter_api()     # Get the Authenticated Api
    # Draw the header using data of PINNED_TWEET_ID
    draw_header(get_status_data(api, PINNED_TWEET_ID))
    api.update_profile_banner(os.path.join(
        parent_directory, 'header.png'))  # Upload the header
