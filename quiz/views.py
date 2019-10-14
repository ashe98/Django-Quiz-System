from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,
        'quiz/home.html',)

def questions(request, quiz_name = ""):
    #print(quiz_name)
    if request.method == 'GET':
        u = Scores()
        u.noq = Quiz.objects.filter(quiz_name__exact = quiz_name)[0]
        u.test_taker = request.user
        u.save()
        ques = Quiz.objects.filter(quiz_name__exact = quiz_name)
        qu = []
        qu += ques
        ques = ques[0].qs.all()
        #print(qu)
        #ques = Questions.objects.filter(catagory__exact = choice)
        return render(request,
            'quiz/questions.html',
            {'ques':ques,
            'quizname':qu})
    elif request.method == 'POST':
        n = request.user.username
        data = request.POST
        datas = dict(data)
        print(datas)
        qid = []
        qans = []
        ans = []
        score = 0
        for key in datas:
            try:
                qid.append(int(key))
                qans.append(datas[key][0])
            except:
                print("Csrf")
        for q in qid:
            ans.append((Questions.objects.get(id = q)).answer)
        total = len(ans)
        for i in range(total):
            if ans[i] == qans[i]:
                score += 1
        # print(qid)
        # print(qans)
        # print(ans)
        #u = Scores.objects.filter()
        for i in range(0, Scores.objects.count()):
            print(i, Scores.objects.all()[i].quizname)
            if Scores.objects.all()[i].getusername == request.user.username:
                u = [Scores.objects.all()[i]]
        u[0].scoreofu = score
        u[0].save()
        print(score)
        return HttpResponseRedirect(reverse('home'))
    
def about(request):
    return render(request,
        'quiz/about.html')

def createquiz(request):
    if request.method == 'GET':
        return render(request,
            'quiz/create.html')
    elif request.method == 'POST':
        q = Quiz()
        q.created_by = request.user
        q.quiz_name = request.POST['quizname']
        q.save()
        mm = (int)(request.POST['mm'])
        print(type(mm))
        print(q.quiz_name, mm)
        ob = Questions.objects.all()
        arr = []
        for i in range(0, len(ob)):
            arr += [Questions.objects.all()[i].marks]
        print(arr)
        li = subset_sum_problem(arr, mm)
        while (True):
            if(li == []):
                mm -= 1
                li = subset_sum_problem(arr, mm)
            else:
                break
        li = li[0]
        visited = []
        for i in range(0, len(li)):
            for j in range(0, Questions.objects.count()):
                if li[i] == Questions.objects.all()[j].marks and j not in visited:
                    visited += [j]
                    q.qs.add(Questions.objects.all()[j])
                    break
        q.save()
        return HttpResponseRedirect(reverse(home))


def addqn(request):
    if request.method == 'POST':
        qn = request.POST['question']
        optiona = request.POST['optiona']
        optionb = request.POST['optionb']
        optionc = request.POST['optionc']
        optiond = request.POST['optiond']
        answer = request.POST['answer']
        marks = request.POST['marks']

        q = Questions()
        q.question = qn
        q.optiona = optiona
        q.optionb = optionb
        q.optionc = optionc
        q.optiond = optiond
        q.answer = answer
        q.marks = marks

        q.save()
        return HttpResponseRedirect(reverse('create_quiz'))
    else:
        return render(request,
            'quiz/addqn.html')

def select(request):
    n = request.user.username
    print(n)
    quizs = Quiz.objects.all()[0].getusername
    print(quizs)
    quizzes_names = []
    for i in range(0, Quiz.objects.count()):
        print(i, Quiz.objects.all()[i].getusername)
        if Quiz.objects.all()[i].getusername == n:
            quizzes_names += [Quiz.objects.all()[i]]
    #quizzes_names = [obj for obj in Quiz.objects.all() if obj.getusername == 'n']
    print(quizzes_names)
    return render(request,
        'quiz/selectquizzes.html',
        {'quizzes_names' : quizzes_names})

def score(request, quiz_name):
    soq = []
    for i in range(0, Scores.objects.all().count()):
        if Scores.objects.all()[i].quizname == quiz_name:
            soq += [Scores.objects.all()[i]]
    print(soq)
    return render(request,
        'res/viewresult.html',
        {'soq' : soq})

def takequiz(request):
    quizzes_names = Quiz.objects.all()
    print(quizzes_names)
    return render(request,
        'quiz/takequiz.html',
        {'quizzes_names' : quizzes_names})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request,
                'quiz/login.html', {'error':"Invalid Credentials!"})
    else:
        return render(request,
            'quiz/login.html',
             {'msg' : 'Logged in Successfully!'})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


#utility functions
def subset_sum_problem_help(number, hashed_array, hash_store, used):
    if (number == 0):
        hash_store[tuple(used)] = used
    elif(number > 0):
        for each in hashed_array:
            for i in range(int(hashed_array[each])):
                new_hashed_array = hashed_array.copy()
                new_hashed_array[each] -= 1
                new_num = number - each
                subset_sum_problem_help(new_num, new_hashed_array, hash_store, used + [each])


def subset_sum_problem(arr, num):
    hash_store = {}
    hashed_array = {}
    for each in arr:
        if(each not in hashed_array):
            hashed_array[each] = 1
        else:
            hashed_array[each] += 1
    subset_sum_problem_help(num, hashed_array, hash_store, [])
    return list(hash_store.values())

#
#
#
#
#
#
#
