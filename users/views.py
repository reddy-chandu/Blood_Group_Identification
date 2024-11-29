from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
import base64
import cv2
import numpy as np


# home page view
def home(request):
    if(request.user.is_authenticated):
        return redirect('/profile')
    else:
        return render(request,'home.html')

# sign in page view
def signin(request):
    if(request.user.is_authenticated):
        return redirect('/profile')
    if(request.method == 'POST'):
        username1 = request.POST['username']
        password1 = request.POST['password']
        user = authenticate(request,username=username1,password=password1)
        if(user != None):
            login(request,user)
            return redirect('/profile')
        else:
            msg = 'Invalid Username/Password'
            return render(request, 'login.html',{'msg':msg})
    else:
        return render(request,'login.html')

# sign up page view
def signup(request):
    if(request.user.is_authenticated):
        return redirect('/profile')
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            un = form.cleaned_data.get('username')
            ps = form.cleaned_data.get('password1')
            user = authenticate(username=un,password=ps)
            return redirect('/signin')
        else:
            return render(request,'signup.html',{'err':form.errors})
    else:
        return render(request,'signup.html')

# profile page view
def profile(request):
    if(request.method == "POST"):
         if(request.FILES.get("abo")):
             img_name = request.FILES["abo"].read()
             encode = base64.b64encode(img_name).decode('utf-8')
             img_url = f"data:image/jpg;base64,{encode}"
             abo_img = cv2.imdecode(np.frombuffer(img_name, np.uint8), cv2.IMREAD_COLOR)
             grey = cv2.cvtColor(abo_img,cv2.COLOR_BGR2GRAY)
             blur = cv2.GaussianBlur(grey,(5,5),0)
             enhance = cv2.equalizeHist(blur)
             var, bin_img = cv2.threshold(enhance,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
             kernel_imp = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
             bin_img = cv2.morphologyEx(bin_img,cv2.MORPH_OPEN,kernel_imp)
             bin_img = cv2.morphologyEx(bin_img,cv2.MORPH_CLOSE,kernel_imp)

             var, img = cv2.imencode('.jpg',bin_img)
             mor_img = base64.b64encode(img).decode('utf-8')
             mor_img_url = f"data:image/jpeg;base64,{mor_img}"
             hei,wid = bin_img.shape
             mid_wid = wid//3
 
             region_A = bin_img[:, 0:mid_wid]
             region_B = bin_img[:, mid_wid:2*mid_wid]
             region_D = bin_img[:, 2*mid_wid:]
 
             def cal_agg(region):
                num_labels,labels,stats,var = cv2.connectedComponentsWithStats(region,connectivity=8)
                return num_labels-1
           
             num_region_A = cal_agg(region_A)
             num_region_B = cal_agg(region_B)
             num_region_D = cal_agg(region_D)

             obj = ''
             if (num_region_A>0 and num_region_B==0):
                obj = 'A'
             elif (num_region_A==0 and num_region_B>0):
                obj = 'B'
             elif (num_region_A>0 and num_region_B>0):
                obj = 'AB'
             elif (num_region_A==0 and num_region_B==0):
                obj = 'O'
             else:
                obj = 'Unknown'
             if(num_region_D>0):
                obj += ' Positive'
             else:
                obj += ' Negative'
              
             return render(request, 'profile.html', {'img': img_url, 'mor_img': mor_img_url,'obj':obj})
    elif(request.user.is_authenticated):
        return render(request,'profile.html')
    else:
        return redirect('/signin')

# signout
def signout(request):
    logout(request)
    return redirect('/')