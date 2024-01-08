from django.shortcuts import render, HttpResponse
from django.http.response import StreamingHttpResponse
from autorehab.camera import IPWebCam


posts = [
    {
        'author': 'ihFahn',
        'title' : 'What is this?',
        'content' : 'On the 31st of August in 2023, the 66th Malaysia Independence Day, I torn my ACL. This is an app developed to specifically help me in my ACL rehabs. '
    }

]


def exerciseList(x):
    if x == 1:
        return "Front Straight Leg Raise"
    if x == 2:
        return "Side Straight Leg Raise"
    if x == 3:
        return "Pronated Hip Extension"
    if x == 4:
        return "Inner Quadriceps Range"
    


# Create your views here.
def home(request):

    context = {
        'posts' : posts
    }

    return render(request, 'autorehab/home.html', context)

def home_dev(request):

    context = {
        'url':"home",
        'title':'Home',
        'general' : 'Physiotherapy',
        'appName' : 'REHABIBI',
        'author' : 'by: ihFahn',
        'getStarted' : 'Get Started'
    }

    return render(request, 'autorehab/home_dev.html', context)

def detection(request):
    return HttpResponse("detection page")

def setup(request):
    return render(request, 'autorehab/setup.html', {'title': 'Setting it Up'})

def setup_dev(request):

    context = {
        'bigTitle' : 'Select your exercise',
        'exercise1' : 'Front Straight Leg Raise',
        'exercise2' : 'Side Straight Leg Raise',
        'exercise3' : 'Pronated Hip Extension',
        'exercise4' : 'Inner Quadriceps Range'
    }



    return render(request, 'autorehab/setup_dev.html', context)

def durrep_dev(request):

    context = {
    
        'midTitle' : 'Setting it up',
        'duration' : 'Duration',
        'reps' : 'Reps'

    } 
    if request.method == 'POST': #this is coming from setup_dev
        exerciseType = request.POST.get('exerciseType')
        request.session['exerciseType'] = int(exerciseType)
        context['exerciseType'] = exerciseList(int(exerciseType))

    return render(request, 'autorehab/durrep_dev.html', context)

def detection_dev(request):


    # exerciseNumber = request.session.get('exerciseType', None)
    # if exerciseNumber == None:
    exerciseNumber = int(request.POST.get('exerciseType'))
    if exerciseNumber == 1:
        exerciseType = 'Front Straight Leg Raise'
    if exerciseNumber == 2:
        exerciseType = 'Side Straight Leg Raise'
    if exerciseNumber == 3:
        exerciseType = 'Pronated Hip Extension'
    if exerciseNumber == 4:
        exerciseType = 'Inner Quadriceps Range'
    
    



    context = {

        'exerciseType' : exerciseType,

    }

    
    if request.method == 'POST': #this is coming from setup_dev
        duration = request.POST.get('durationNumber')
        reps = request.POST.get('repsNumber')

        request.session['duration'] = duration
        context['duration'] = duration
        request.session['reps'] = reps
        context['reps'] = reps

    return render(request, 'autorehab/detection_dev.html', context)

def dashboard(request):

    context = {
        'url':"dashboard",
        'title':'Dashboard',
        'bigTitle' : 'Select your exercise',
        'exercise1' : 'Front Straight Leg Raise',
        'exercise2' : 'Side Straight Leg Raise',
        'exercise3' : 'Pronated Hip Extension',
        'exercise4' : 'Inner Quadriceps Range'
    }

    return render(request, 'autorehab/dashboard.html', context)

def our_team(request):
    context={
        'url':"our_team",
        'title':"Our Team"
    }

    return render(request,'autorehab/our_team.html',context)

def exercise(request):

    context = {
        'url':"exercise",
        'title':'Exercise',
        'bigTitle' : 'Select your exercise',
        'exercise1' : 'Front Straight Leg Raise',
        'exercise2' : 'Side Straight Leg Raise',
        'exercise3' : 'Pronated Hip Extension',
        'exercise4' : 'Inner Quadriceps Range'
    }

    return render(request, 'autorehab/exercise.html', context)

import zlib
import base64
def gen(camera):
    print('gen here')
    while True:
        frame, elapsed_time, reps = camera.get_frame()
        # print(int(elapsed_time))
        # print(type(frame))
    
        # boundary_section = (
        #     b'--frame\r\n'
        #     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        #     b'Elapsed-Time: ' + str(elapsed_time).encode('utf-8') + b'\r\n\r\n'
        # )
            # Compress the bytes using gzip
        # compressed_bytes = zlib.compress(frame.encode('utf-8'))

        # Convert the compressed bytes to a base64-encoded string
        # compressed_str = base64.b64encode(compressed_bytes).decode('utf-8')
        # boundary_section = (
        #     b'--frame\n'
        #     b'frame:' + frame.encode('utf-8') + b'\n'
        #     b'time:' + str(elapsed_time).encode('utf-8')
        # )
        data = {
            "frame": frame,
            "time": elapsed_time,
            "reps": reps
        }
        json_str = json.dumps(data)
        # return frame, elapsed_time
        yield f"data: {json_str}\n\n"
        # yield boundary_section
        
import json
from django.http import JsonResponse

def webcam_feed(request):
    print('here')
    webcamInstance = IPWebCam(request.session.get('exerciseType', None), 
                                              request.session.get('duration', None), 
                                              request.session.get('reps', None))
    
    # elapsed_time = webcamInstance.timeGetter()
    # print(elapsed_time)
    response =  StreamingHttpResponse(gen(webcamInstance),
                                 content_type='text/event-stream')

    # response =  StreamingHttpResponse(gen(webcamInstance),
    #                              content_type='multipart/x-mixed-replace; boundary=frame')
    return response