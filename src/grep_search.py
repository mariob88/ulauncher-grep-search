import logging as log

from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent
from .queryevent import KeywordQueryEventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction

logger = log.getLogger(__name__)

class grep_search(Extension):
    ICON = 'images/main_icon.png'

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
    
    def menu(self):
        kw = self.preferences['kw']
        items = []

        items.append(
            ExtensionResultItem(name = "Write a string to search",
                                description = "To perform a search, write a string following with a space and a path if you want to specify where to perform the search. Otherwise, the default path will be used.",
                                icon = 'images/search.png',
                                on_enter = DoNothingAction()))
        
        return RenderResultListAction(items)