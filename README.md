# Twitter-Header-Script

Python Script to generate a Twitter Header with Like / Retweet Statistics of a Tweet, and 3 latest followers

## Demo

![header.png](.github/header.png)
Sample Generated Image

Also, I am going to be using this as [my header on Twitter](https://twitter.com/HAliPunjabi) for a while, using [this tweet](https://twitter.com/HAliPunjabi/status/1435219303465324548).

## Usage

1. Download the requirements  
   `pip install -r requirements.txt`
2. Create a directory called fonts and download SourceCodePro-Regular.ttf from [Google Fonts](https://fonts.google.com/specimen/Source+Code+Pro) into it
3. Create a Twitter app from [Twitter Developer Dashboard](https://developer.twitter.com/)
4. Rename `.env.sample` to `.env` and fill it with appropriate values from your Twitter App
5. Change the `PINNED_TWEET_ID` variable in `main.py` to the ID of the tweet you want to use
6. Run the script to generate the header and upload it
7. Run it at regular intervals (e.g, using cronjobs) to make sure the header is always updated
