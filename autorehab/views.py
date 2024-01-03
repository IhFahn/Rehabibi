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
        'general' : 'Physiotherapy',
        'title' : 'An acl rehab application',
        'appName' : 'AutoRehab',
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


    exerciseNumber = request.session.get('exerciseType', None)
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

def gen(camera):
    while True:
        frame, elapsed_time = camera.get_frame()
        #print(int(elapsed_time))
        boundary_section = (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
            b'Elapsed-Time: ' + str(elapsed_time).encode('utf-8') + b'\r\n\r\n'
        )
        
        yield boundary_section
        



def webcam_feed(request):
    webcamInstance = IPWebCam(request.session.get('exerciseType', None), 
                                              request.session.get('duration', None), 
                                              request.session.get('reps', None))
    
    elapsed_time = webcamInstance.timeGetter()
    print(elapsed_time)
    return StreamingHttpResponse(gen(webcamInstance),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
