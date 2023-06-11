
import os
from django.shortcuts import render
# import pytesseract
# import cv2
# import re
# from django.contrib.auth.decorators import login_required
from credential.models import face_reg
# import numpy as np
# from PIL import Image, ImageEnhance, ImageFilter
# from .models import product
# from .models import team

# @login_required


def home(request):
    username = request.session.get('username')  # Retrieve the username from session
    user = face_reg.objects.filter(username=username).first()
          

    return render(request, 'index.html', {'user': user})



