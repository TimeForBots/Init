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
# Description	: Simple start/restart/stop script for TimeForBots
# TODO 			: Replace this with systemctl

SERVER_TOP=..

if [[ ! -z $2 ]]; then
	SERVER_TOP=$2
fi

export PYTHONPATH=$SERVER_TOP/:$SERVER_TOP/Bots:$SERVER_TOP/Methods:$PYTHONENV

echo $PYTHONENV

# Start Sever
if [[ -z $1 || $1 == "start" ]]; then
	python TimeForUpdates.py $SERVER_TOP/Bots/configs &

# Stop server
elif [[ $1 == "stop" ]]; then
	pkill -f TimeForUpdates.py

# Restart server
elif [[ $1 == "restart" ]]; then
	sh $0 stop
	sh $0 start

else
	echo "sh TimeForBots.sh [start  | stop | restart]"
fi
