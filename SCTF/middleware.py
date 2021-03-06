from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

from constance import config


class FilterRequestByGameStateMiddlewareMixin(MiddlewareMixin):

    def process_request(self, request):
        if config.GAME_STATUS == settings.GAME_STATUS_PAUSE and 'game_paused' not in request.path and 'game_start' not in request.path:
            return redirect('game_paused_view')

        if config.GAME_STATUS == settings.GAME_STATUS_FINISH and 'game_stopped' not in request.path and 'game_start' not in request.path:
            return redirect('game_stopped_view')

        if 'challenge' in request.path and config.GAME_STATUS != 'PLAY':
            return redirect('/')