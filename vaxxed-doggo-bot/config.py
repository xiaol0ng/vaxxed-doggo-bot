import os
import json

token = os.getenv("token")

if not token:
    print("No token found.")
    os._exit(0)


solscan_headers = {
    "Host": "api.solscan.io",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
}

# Data
data_file = "data/data.json"
if not os.path.exists(data_file):
    with open(data_file, "w") as f:
        json.dump({}, f)

# Doggos Metadata
doggos = json.load(open("vaxxed-doggo-bot/assets/doggos.json"))

# Owner Address
owner_address_magic_eden = "GUfCR9mK6azb9vcpsxgXyj7XRPAKJd4KMHTTVvtncGgp"
owner_address_solanart = "3D49QorJyNaL4rcpiynbuS3pRH4Y7EXEM6v6ZGaqfFGK"

# Doggo Info
allowed_show_doggo_info_channels = [
    "memes",
    "general",
    "bot-commands",
    "share-your-nft",
    "magiceden-listings",
    "chat",
]

# Scam Detector
allowed_check_scam_channels = [
    "memes",
    "general",
    "bot-commands",
    "share-your-nft",
    "magiceden-listings",
    "chat",
]

# Doggo Market stats
allowed_show_doggo_market_stats_channels = [
    "memes",
    "general",
    "bot-commands",
    "share-your-nft",
    "magiceden-listings",
    "chat",
]


# Memes
allowed_meme_channels = [
    "memes",
    "general",
    "bot-commands",
    "share-your-nft",
    "magiceden-listings",
    "chat",
]

# Solana Market stats
allowed_show_solana_market_stats_channels = [
    "memes",
    "general",
    "bot-commands",
    "share-your-nft",
    "magiceden-listings",
    "chat",
]

# Show Commands
allowed_show_help_channels = [
    "memes",
    "general",
    "bot-commands",
    "share-your-nft",
    "magiceden-listings",
    "chat",
]
