import logging as log
import subprocess
import re
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

logger = log.getLogger(__name__)

class KeywordQueryEventListener(EventListener):

    def __init__(self):
        self.FILE_ICON = 'images/file.png'
        self.ERROR = 'images/error.png'

    def on_event(self, event, extension):
        query = event.get_argument() or ""
        items = []
        timeout = extension.preferences['default_timeout']

        if not query:
            return extension.menu()
        
        if "\"" in query or "\'" in query:
            pattern = r"(\'|\")(.*)(\'|\")"
            search_string = re.search(pattern, query).group(2)
            logger.info(search_string)
            query_path = query.rsplit(maxsplit=1)[-1]
            path = extension.preferences['default_path'] if not query_path else query_path

        else:
            query_list = query.split(maxsplit=1)
            search_string = query_list.pop(0)
            path = extension.preferences['default_path'] if not query_list  else query_list.pop(0)

        grep_cmd = [
            'timeout', timeout, 'grep', '-r', '-I', search_string, path
            ]

        logger.info(grep_cmd)

        cut_cmd = ['cut', '-c1-500']

        grep = subprocess.Popen(grep_cmd,
                                   stdout=subprocess.PIPE
                                   )

        cut =  subprocess.Popen(cut_cmd,
                                    stdin=grep.stdout, 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        
        out, err = cut.communicate()

        if err:
            logger.error(err)
            items.append(
                ExtensionResultItem(name = 'Error',
                                description = err,
                                icon = self.ERROR,
                                on_enter = HideWindowAction())
            )
            return RenderResultListAction(items)

        result = out.split('\n'.encode())
        result = list([r for r in result if r])

        if not result:
            items.append(
                ExtensionResultItem(name = 'No results',
                                description = 'No files found with your search string',
                                icon = self.ERROR,
                                on_enter = HideWindowAction())
            )
            return RenderResultListAction(items)

        for r in result[:10]:
            file, match = r.decode('UTF-8').split(':', maxsplit=1)
            items.append(
                ExtensionResultItem(name = file,
                                description = match,
                                icon = self.FILE_ICON,
                                on_enter = OpenAction(file)))
            
        return RenderResultListAction(items)