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

from datetime import datetime
from Botconfig import botcfg
from Binder import bind, isBinded, getBindFromList

BOT_CONFIGS_DIR = sys.argv[1]

# Array of bots (increases by every bot configuration)
configs = []
binds = []

def charsInStr(string, char) :
	prev = 0
	i = 0

	while True :
		prev = string.find(char, prev)
	
		if prev == -1 :
			return i

		prev += 1
		i += 1

# Setup configs
for cfg in os.listdir(BOT_CONFIGS_DIR) :
	configs.append(botcfg(BOT_CONFIGS_DIR + '/' + cfg))

# Send boot messages
for config in configs :
	if config.bootmsg and config.bootmsgChats :
		for chat_id in config.bootmsgChats :
			config.exportBot().sendMessage(chat_id, config.bootmsg)

lastBotUpdateDate = datetime.now()

while True :
	for config in configs :
		bot = config.exportBot()
		updates = bot.getUpdates(offset=-1)

		# Poll for updates
		if updates and updates[-1].message and updates[-1].message.text and updates[-1].message.date > lastBotUpdateDate :
			cmd = updates[-1].message.text
			
			# Check for bind
			if cmd.split()[0] == "/bind" and charsInStr(cmd, '/') == 3 :
				bindStart = cmd.find('/', 1) + 1
				commandStart = cmd.find('/', bindStart)

				bindstr = cmd[bindStart:commandStart].strip()

				if not config.includesMethod(bindstr.split()[0][0:len(bindstr.split()[0])]) and not isBinded(binds, bindstr) :
					commandstr = cmd[commandStart + 1:len(cmd)].strip()
					binds.append(bind(bindstr, commandstr))
					bot.sendMessage(updates[-1].message.chat_id, 'Successfully binded "' + bindstr + '" to "' + commandstr + '"')
				else :
					bot.sendMessage(updates[-1].message.chat_id, "Bind already reserved by another bind or method!")
			
			elif cmd.split()[0] == "/unbind" and charsInStr(cmd, '/') == 2 :
				bindstr = cmd[cmd.find('/', 1) + 1:len(cmd)]

				delbind = getBindFromList(binds, bindstr)
				if delbind :
					binds.remove(delbind)
					bot.sendMessage(updates[-1].message.chat_id, 'Successfully unbinded "' + bindstr + '"')
				else :
					bot.sendMessage(updates[-1].message.chat_id, '"' + bindstr + '" is not binded' )

			else :
				msg = updates[-1].message.text[1:len(updates[-1].message.text)]

				if isBinded(binds, msg) :
					msg = getBindFromList(binds, msg).command
				
				args = msg.split()

				if config.includesMethod(args[0]) :
					importlib.import_module(args[0]).TimeFor(config, updates[-1], args)
		
			lastBotUpdateDate = updates[-1].message.date
