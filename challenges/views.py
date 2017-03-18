from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from datetime import timedelta
from team.models import Team
from .forms import SubmissonForm
from .models import Category, Challenge, Hint, ChallengeSeen, SolvedChallenge, WrongSubmisson, ChallengeFile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



def start(request):
    if not request.user.is_staff:
        return HttpResponse("HAHAHAHHAHAHAH")

    numChallenges = Challenge.objects.filter(rank = 1).count()
    challenges = Challenge.objects.filter(rank = 1)
    teams = Team.objects.all()

    for x in range(numChallenges):
        challenges[x].unlockedBy.add(*teams)

    return HttpResponse("And so it begun!")

@login_required
def index(request):
    if not hasattr(request.user, 'teammember'):
        return render(request, 'user/index.html',
                {'base':'base.html', 'user':request.user})
    team = request.user.teammember.team
    noOfCategories = Category.objects.all().count()
    categoryInfos = noOfCategories * [None]

    for x in range(noOfCategories):
        category = Category.objects.all()[x]

        solved = Challenge.objects.filter(solvedchallenge__team = team, 
                cat = category)
        unlocked = Challenge.objects.filter(unlockedBy = team, 
                cat = category).exclude(solvedchallenge__team = team)
        categoryInfos[x] = {'name':category.name, 'solved':solved,
                'challenges':unlocked}
        if team.unlocks > 0:
            toUnlock = Challenge.objects.filter(cat = category).exclude(
                    unlockedBy = team).order_by('rank')
            categoryInfos[x]['unlockables'] = toUnlock

    return render(request, 'challenges/index.html', 
            {'base':'base.html', 'category':categoryInfos, 'user':request.user})

@login_required
def file(request, challengeid, filePath):
    teamobj = request.user.teammember.team
    if not (ChallengeSeen.objects.filter(team = teamobj,
        challenge = challengeid).exists()):
        return HttpResponseRedirect(reverse('challenges:index'))
    
    demandedFile = ChallengeFile.objects.filter(challenge = challengeid,
            remotePath = filePath)
    if demandedFile.exists():
        f = open(demandedFile.get().localPath, 'rb')
        response = HttpResponse(f, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + demandedFile.get().fileName
        f.close()
        return response
    return HttpResponseRedirect('challenges:index')



@login_required
def challenge(request, challengeid):
    teamobj = request.user.teammember.team
    if not (Challenge.objects.filter(unlockedBy = teamobj,
        id = challengeid).exists()):
        return HttpResponseRedirect(reverse('challenges:index'))

    chalobj = Challenge.objects.get(id = challengeid)

    if not ChallengeSeen.objects.filter(team = teamobj, challenge__id = challengeid).exists():
        ChallengeSeen(time=timezone.now(), team = teamobj, challenge = chalobj).save()

    usedHints = Hint.objects.filter(usedBy = teamobj, 
            challenge = challengeid).order_by('penalty')
    nextHint = Hint.objects.exclude(usedBy = teamobj
            ).order_by('penalty').filter(challenge = challengeid)
    solved = SolvedChallenge.objects.filter(team = teamobj,
            challenge = chalobj).exists()
    entryForm = SubmissonForm()
    seenSince = ChallengeSeen.objects.get(team=teamobj,
                    challenge=chalobj).time
    if request.method == 'GET':
        return render(request, 'challenges/challenge.html',
                {'base':'base.html', 'form':entryForm, 'seen':seenSince,
                    'lockedHint':nextHint, 'unlockedHints':usedHints,
                    'challenge':chalobj, 'solved':solved, 'user':request.user})
    else:
        submittedSolution = SubmissonForm(request.POST)
        submittedSolution.is_valid()
        if solved:
            return HttpResponseRedirect(reverse('challenges:index'))
        if chalobj.solution == submittedSolution.cleaned_data['solution']:
            teamobj.unlocks += 1
            teamobj.save()
            numWrong = WrongSubmisson.objects.filter(team = teamobj, 
                    challenge = chalobj).count()
            numHints = Hint.objects.filter(challenge = chalobj, usedBy = teamobj)
            penWrong = 0.05
            totHintPen = 1
            for x in range(numHints.count()):
                totHintPen *= 1 - numHints[x].penalty / 100
            totPen = 1 - ((1 - penWrong) ** numWrong) * totHintPen
            eta = timedelta(minutes=chalobj.eta)
            estimatedSolve = eta.total_seconds()
            actualSolve = (timezone.now() - seenSince).total_seconds()
            actualSolve = 1 if actualSolve < 1 else actualSolve
            #factor = estimatedSolve / (actualSolve + totPen)
            factor = 1 - totPen
            baseFactor = estimatedSolve / actualSolve
            baseScore = (int)(chalobj.eta)
            score = (int)(baseScore * factor)
            penal = baseScore - score
            SolvedChallenge(user = request.user, team = teamobj,
                    challenge = chalobj, time = timezone.now(),
                    points = score, totalPenalty = penal).save()
            chalobj.unlockedBy.add(*Team.objects.all())
            curRank = chalobj.rank
            curCat = chalobj.cat
            if Challenge.objects.filter(rank = curRank+1, cat = curCat).exists():
                for x in Challenge.objects.filter(rank = curRank+1, cat = curCat):
                    x.unlockedBy.add(teamobj)
            return render(request, 'challenges/challenge.html',
                    {'base':'base.html', 'unlockedHints':usedHints,
                        'challenge':chalobj, 'solved':solved, 
                        'message':"Nicely done!", 'user':request.user})
        else:
            WrongSubmisson(user = request.user, team = teamobj,
                challenge = chalobj, time = timezone.now(),
                text = submittedSolution.cleaned_data['solution']).save()
            submittedSolution.add_error('solution', "Wrong")
            return render(request, 'challenges/challenge.html',
                    {'base':'base.html', 'form':submittedSolution,
                        'lockedHint':nextHint, 'unlockedHints':usedHints,
                        'challenge':chalobj, 'solved':solved, 'user':request.user})
@login_required 
def unlock(request, challengeid):
    teamobj = request.user.teammember.team
    if teamobj.unlocks < 1:
        return HttpResponseRedirect(reverse('challenges:index'))
    if not Challenge.objects.filter(id=challengeid).exists():
        return HttpResponseRedirect(reverse('challenges:index'))
    ran = Challenge.objects.get(id=challengeid)
    if not Challenge.objects.filter(cat=ran.cat,
        rank=ran.rank-1, unlockedBy = teamobj).exists():
        return HttpResponseRedirect(reverse('challenges:index'))
    teamobj.unlocks -= 1
    teamobj.save()
    Challenge.objects.get(id=challengeid).unlockedBy.add(teamobj)
    return HttpResponseRedirect(reverse('challenges:index'))

@login_required
def hint(request, challengeid):
    teamobj = request.user.teammember.team
    if not (Challenge.objects.filter(unlockedBy = teamobj,
        id = challengeid).exists()):
        return HttpResponseRedirect(reverse('challenges:index'))
    if SolvedChallenge.objects.filter(challenge = challengeid, team = teamobj):
        return HttpResponseRedirect(reverse('challenges:index'))
    hints = Hint.objects.filter(challenge = challengeid).exclude(
        usedBy = teamobj).order_by('penalty')
    if hints.exists():
        hints[0].usedBy.add(teamobj)
    return HttpResponseRedirect('../')

