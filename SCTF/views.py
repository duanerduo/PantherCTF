import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from SCTF.utils import game_end_datetime, set_game_duration
from accounts.models import Team
from challenges.models import Challenge
from cities_light.models import Country
from constance import config



def index(request):
    user = request.user

    countries = Country.objects\
        .annotate(num_user=Count('userprofile'))\
        .filter(num_user__gt=0)

    parameters = {
        'users_count': get_user_model().objects.count(),
        'teams_count': Team.objects.count(),
        'challenges_count': Challenge.objects.count(),
        'total_points_count': Challenge.objects.total_points(),
        'user_points_count': user.profile.total_points,
        'countries_users': json.dumps({c.code2.lower(): c.num_user for c in countries}),
        'config': config,
        'game_end_datetime': game_end_datetime()
    }
    return render(request, 'sctf/base.html', parameters)


@user_passes_test(lambda u: u.is_superuser)
def game_play(request):
    if config.GAME_STATUS == 'SETUP':
        # TODO manage game start
        pass
    elif config.GAME_STATUS == 'PAUSE':
        # TODO manage game resume
        pass
    else:
        return redirect(request.path)

    config.GAME_STATUS = 'PLAY'
    config.GAME_START_DATETIME = datetime.now()
    return redirect(request.path)


@user_passes_test(lambda u: u.is_superuser)
def game_pause(request):
    if config.GAME_STATUS == 'START':
        # TODO manage game start
        pass
    else:
        return redirect(request.path)

    config.GAME_STATUS = 'PAUSE'
    set_game_duration(datetime.now() - config.GAME_START_DATETIME)
    return redirect(request.path)


class ChangeGameStaus(APIView):
    # TODO superuser required
    # TODO only post

    def post(self, request, **kwargs):
        status = request.data.get('status')
        if status not in settings.GAME_STATUS_CHOICES_NAMES:
            return Response('Invalid status.', status=400)

        if config.GAME_STATUS == 'FINISH':
            return Response('Game is finished', status=400)

        if status == 'SETUP':
            return Response('Cannot set SETUP', status=400)

        if status == config.GAME_STATUS:
            return Response('Same status', status=400)

        if status == 'PLAY':
            if config.GAME_STATUS == 'SETUP':
                # TODO manage game start
                pass
            elif config.GAME_STATUS == 'PAUSE':
                # TODO manage game resume
                pass

            config.GAME_STATUS = 'PLAY'
            config.GAME_START_DATETIME = datetime.now()

            # TODO manage game
            return Response('Same status', status=200)



