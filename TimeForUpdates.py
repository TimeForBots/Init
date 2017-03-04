# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author 		: Patrick Pedersen <ctx.xda@gmail.com>
# Last updated  : 18:30 3/3/2017 CEST
# Description	: Handles polling routine on bot updates

import sys
import os
import importlib
from Botconfig import botcfg

BOT_CONFIGS_DIR = sys.argv[1]

# Array of bots (increases by every bot configuration)
configs = []

# Setup configs
for cfg in os.listdir(BOT_CONFIGS_DIR) :
	configs.append(botcfg(BOT_CONFIGS_DIR + '/' + cfg))

# Send boot messages
for config in configs :
	if config.bootmsg and config.bootmsgChats :
		for chat_id in config.bootmsgChats :
			config.exportBot().sendMessage(chat_id, config.bootmsg)

lastBotUpdateId = [len(configs)]

while True :
	update_count = 0

	for config in configs :
		bot = config.exportBot()
		updates = bot.getUpdates()

		# Poll for updates
		if updates and updates[-1].update_id != lastBotUpdateId[update_count] :
			arg = updates[-1].message.text[1:len(updates[-1].message.text)].split()
			if config.includesMethod(arg[0]) :
				importlib.import_module(arg[0]).TimeFor(config, updates[-1], arg)
		
			lastBotUpdateId[update_count] = updates[-1].update_id

		update_count += 1
