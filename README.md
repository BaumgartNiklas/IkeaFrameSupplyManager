# IkeaFrameSupplyManager
### A Warframe Dojo Bot

 This is a small discord bot, meant to be self-hosted, that helps you to exploit your clan mates
by showing them exactly which decorations and resources are currently required in the dojo.

## Usage:
1. Create a new discord bot and put your token into the config.json
2. Invite your new bot to your server
3. Write `/sync` in a text channel to load the commands
4. Set permissions for the commands
5. Add the decorations and resources you need in the dojo via commands
6. Profit!

## Commands:
- `/listdeco` Lists all currently requested decorations and resources
- `/donatedeco name amount` Tells the bot that a decoration or resource has been donated.
<br> If the total donated amount exceeds the requested amount, the entry is removed from the list.
- `/requestdeco name amount [Optional]priority` Adds a decoration or resource to the list
<br> Optionally, a priority can be specified (0, 1, 2) with 0 being low and 2 being high priority.
<br> That way people can see what is required soon and what is just a "nice to have".
- `/removedeco name` Removes a decoration or resource from the list
