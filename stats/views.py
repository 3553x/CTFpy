from django.shortcuts import render
from team.models import Team
from challenges.models import SolvedChallenge, Challenge, Category, WrongSubmisson

def index(request):
    return render(request, 'stats/index.html', 
            {'base':'base.html', 'user':request.user})

def teamView(request):
    listOfTeams = [None] * Team.objects.all().count()
    for x in range (len(listOfTeams)):
        currentTeam = Team.objects.all()[x]
        teamName = currentTeam.name
        Points = 0
        for y in SolvedChallenge.objects.filter(team = currentTeam):
            Points += y.points
        listOfTeams[x] = {'name':teamName, 'points':Points, 'id':currentTeam.id}
    sortedList = sorted(listOfTeams, key = lambda arg: arg['points'], reverse = True)
    for x in range(len(listOfTeams)):
        sortedList[x]['rank'] = x + 1        
    return render(request, 'stats/team.html', 
            {'base':'base.html', 'user':request.user, 'teams':sortedList})

def challengeView(request):
    numOfCategories = Category.objects.all().count()
    categoryInfo = [None] * numOfCategories
    for x in range(numOfCategories):
        currentCategory = Category.objects.all()[x]
        categoryName = currentCategory.name
        challenges = Challenge.objects.filter(cat = currentCategory)
        challengeInfo = [None] * challenges.count()
        for y in range(challenges.count()):
            currentChallenge = challenges[y]
            currentName = currentChallenge.name
            numSolvedBy = SolvedChallenge.objects.filter(challenge = currentChallenge).count()
            challengeInfo[y] = {'name':currentName, 'solved':numSolvedBy,
                    'id':currentChallenge.id}
        categoryInfo[x] = {'name':categoryName, 'challenges':challengeInfo}
    return render(request, 'stats/challenge.html',
            {'base':'base.html', 'user':request.user, 'challenges':categoryInfo})


def challengeDetailedView(request, challengeId):
    solvedByTeams = Team.objects.filter(solvedchallenge__challenge = challengeId)
    teamsNum = solvedByTeams.count()
    solvedByInfo = [None] * teamsNum
    name = Challenge.objects.get(id = challengeId).name
    for x in range(teamsNum):
        currentTeam = solvedByTeams[x]
        entry = SolvedChallenge.objects.get(team = currentTeam,
            challenge = challengeId)
        penalty = entry.totalPenalty
        score = entry.points + penalty
        total = entry.points
        solvedByInfo[x] = {'team':currentTeam, 'score':score,
            'penalty':penalty, 'total':total}
    return render(request, 'stats/challenge.html', 
            {'base':'base.html', 'user':request.user, 'details':solvedByInfo,
                'challengeName':name})
