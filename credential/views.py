from django.contrib import messages, auth
from .models import face_reg
from django.shortcuts import render, redirect
import cv2
import time
from .simple_facerec import SimpleFacerec


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = face_reg.objects.filter(username=username, password=password).first()
        if user is not None:
            # Perform any additional logic or checks if needed
            request.session['username'] = username  # Store the username in session
            return redirect('home:home')
    return render(request, 'login.html')

def face_id(request):
    sfr = SimpleFacerec()
    sfr.load_encoding_images("media/userphoto/")

    # Load Camera
    cap = cv2.VideoCapture(0)

    matched = False  # Flag to indicate if a match is found
    match_start_time = None  # Variable to store the start time of the match

    while True:
        ret, frame = cap.read()

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)

        print("Face Locations:", face_locations)
        print("Face Names:", face_names)

       
        for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

                # Check if the captured image is found in the "images" directory
                if name in sfr.known_face_names:
                    matched = True
                    if match_start_time is None:
                        match_start_time = time.time()

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27 or (matched and time.time() - match_start_time >=5):
            break

    if matched:
        request.session['username'] = name  # Store the username in session
        return redirect('home:home')

    cap.release()
    cv2.destroyAllWindows()

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        education = request.POST['education']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        userphoto = request.FILES['userphoto']
        cv = request.FILES['cv']

        User=face_reg

    
                
        if password==cpassword:

            if User.objects.filter(username=username).exists():
                messages.info(request, "username is taken")
                print("username is taken")
                return redirect('face:signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email is taken")
                print("email is taken")
                return redirect('face:signup')
            else:
                user = User(username=username, first_name=first_name, last_name=last_name,address=address,education=education,phone=phone,userphoto=userphoto, cv=cv, email=email, password=password,cpassword=cpassword)
                user.save()
                print("user created")
        else:
            messages.info(request, "password not matching")
            return redirect('face:signup')
        return redirect('face:login')

    return render(request, 'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('/')





# Create your views here.
