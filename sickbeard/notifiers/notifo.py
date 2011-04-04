# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.

import urllib
import sickbeard

from sickbeard import logger, common
from sickbeard.encodingKludge import fixStupidEncodings

try:
    import lib.simplejson as json
except:
    import json


API_URL = "https://%(username)s:%(secret)s@api.notifo.com/v1/send_notification"

class NotifoNotifier:

    def test_notify(self, username, apisecret):
        return self._sendNotifo("This is a test notification from Sick Beard", username, apisecret)

    def _sendNotifo(self, msg, username, apisecret):
        msg = msg.strip()
        apiurl = API_URL % {"username": username, "secret": apisecret}
        # got the hint of encoding to utf-8 from http://stackoverflow.com/questions/787935/python-interface-to-paypal-urllib-urlencode-non-ascii-characters-failing/788055#788055
        # seams like urlencode likes utf-8 better then unicode
        data = urllib.urlencode({
            "msg": msg.encode('utf-8'),
        })

        try:
	    data = urllib.urlopen(apiurl, data)	
            result = json.load(data)
        except IOError:
            return False
        
        data.close()

        if result["status"] != "success" or result["response_message"] != "OK":
            return False
        else:
            return True


    def notify_snatch(self, ep_name):
        if sickbeard.NOTIFO_NOTIFY_ONSNATCH:
            logger.log(u"Preparing snatch notification for " + ep_name, logger.DEBUG)
            self._notifyNotifo(u""+common.notifyStrings[common.NOTIFY_SNATCH]+': '+ep_name)

    def notify_download(self, ep_name):
        if sickbeard.NOTIFO_NOTIFY_ONDOWNLOAD:
            logger.log(u"Preparing download notification for " + ep_name, logger.DEBUG)
            self._notifyNotifo(u""+common.notifyStrings[common.NOTIFY_DOWNLOAD]+': '+ep_name)       

    def _notifyNotifo(self, message=None, username=None, apisecret=None, force=False):
        if not sickbeard.USE_NOTIFO and not force:
            logger.log(u"Notification for Notifo not enabled, skipping this notification", logger.DEBUG)
            return False

        if not username:
            username = sickbeard.NOTIFO_USERNAME
        if not apisecret:
            apisecret = sickbeard.NOTIFO_APISECRET

        logger.log(u"Sending notification for " + message, logger.DEBUG)

        self._sendNotifo(message, username, apisecret)
        return True

notifier = NotifoNotifier
