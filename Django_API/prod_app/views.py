from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import hashlib, pandas as pd
from prod_app.db_config import DbModulee
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from prod_app.carecloud.ccproductivity import CareCloud
from prod_app.mis.misproductivity import MISProd
from prod_app.fox.foxproductivity import FoxProd
from prod_app.globalportal.globalportalproductivity import GPProductiivty
from prod_app.director import GetDirectors
from django.views.decorators.http import require_http_methods
from ProductivityDashboard.settings import key
from functools import wraps
from datetime import datetime, timedelta
import jwt
import traceback
import pdb
import json
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited
import warnings
warnings.filterwarnings('ignore')


db_obj = DbModulee()

def my_rate_limited_view(request):

    return HttpResponse("You are Blocked due to entering incorrect credentials")

def get_encrypted_code(password):
    byte_password = password.encode("ascii")
    sha512_hash = hashlib.sha512(byte_password)
    hash_bytes = sha512_hash.digest()
    return "".join(format(byte, "02X") for byte in hash_bytes)

@csrf_exempt
@require_http_methods(['POST'])
@ratelimit(key='ip', rate='3/m', method='POST', block=True)
def login_view(request):
    try:
        form = request.POST
        username = form['username']
        password = form['password']
        enc_password = get_encrypted_code(password)
        query = f"""
                Select User_Id, Password  from Users where User_Id = '{username}' and Password = '{enc_password}' and is_active = 1
                
                """
        con, cur = db_obj.live_db()
        data = pd.read_sql(query, con)

        if len(data)>0:
            expiry_time = datetime.now() + timedelta(minutes=30)
            payload = {"userName": username, "exp": expiry_time}
            jwt_token = jwt.encode(payload, KEY, algorithm="")
            if isinstance(jwt_token, bytes):
                # If jwt.encode() returns bytes, decode it to string
                jwt_token = jwt_token.decode()
            else:
                # If jwt.encode() returns string, use it directly
                jwt_token = jwt_token
            # jwt_token = jwt.encode({"userName": username}, KEY, algorithm="HS256")
            # jwt_token = jwt_token.decode('utf-8')
            response_data = {'success': True, 'jwt_token': jwt_token}
            return JsonResponse(response_data, safe=False)
            # return JsonResponse({True,jwt_token_list}, safe=False)
        else:
            return HttpResponse(False)
        
    except Exception as e:
        traceback.print_exc()
        print("Exception: login_view,",e)
        return HttpResponse("Error Occur While Login")

def token_required(view_func):
    # pdb.set_trace()

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return HttpResponse('Token is missing', status=401)
        
        if token.startswith('Bearer '):
            token = token[7:]
        try:
            decoded_token = jwt.decode(token,key, algorithms=[''])
            kwargs['username'] = decoded_token.get('userName')
        except jwt.ExpiredSignatureError:
            return HttpResponse('Token has expired', status=401)
        except jwt.InvalidTokenError:
            return HttpResponse('Invalid token', status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view

# @token_required
def protected_route(request, username):
    return HttpResponse(f'Hello, user {username}! This route is protected.')

# @token_required
@csrf_exempt
def carecloud(request, **kwargs):
    # try:
    if request.method == 'POST':
        weeksbefore = request.POST.get('weeksbefore')
        director = request.POST.get('director')
        performance = request.POST.get('performance')
        cc_obj = CareCloud()
        CcProd = cc_obj.CareCloudData(weeksbefore,director,performance)
        if len(CcProd)>0:
            CcProd1 = CcProd.to_dict(orient='records')
            # CcProd1 = CcProd
            # response = JsonResponse(CcProd1, safe=False)
            return JsonResponse(CcProd1, safe=False)
        else:
            return JsonResponse({"Data": "No Data Found"}, safe=False)
    else:
        return HttpResponse("Get Method is not allowed")
    # except Exception as e:
    #     print("Error in Care Cloud Data",e)
    #     return HttpResponse("Error in Care Cloud Data",e)
    

# @token_required
@csrf_exempt   
def mis(request, **kwargs):
    try:
        if request.method == 'POST':
            weeksbefore = request.POST.get('weeksbefore')
            director = request.POST.get('director')
            performance = request.POST.get('performance')
            mis_obj = MISProd()
            MisProd = mis_obj.MisProdSignOff(weeksbefore,director,performance)
            # return HttpResponse(MisProd)
            if len(MisProd)>0:
                MisProd1 = MisProd.to_dict(orient='records')
                return JsonResponse(MisProd1, safe=False)
            else:
                return HttpResponse("No Data Found")
        else:
            return HttpResponse("Get Method is not allowed")
    except Exception as e:
        print("Error in MIS Data",e)
        return HttpResponse("An error occurred while processing the request.")

# @token_required
@csrf_exempt   
def fox(request, **kwargs):
    try:
        if request.method == 'POST':
            weeksbefore = request.POST.get('weeksbefore')
            director = request.POST.get('director')
            performance = request.POST.get('performance')
            fox_obj = FoxProd()
            FoxProductivity = fox_obj.FoxSignOffProd(weeksbefore,director,performance)
            if len(FoxProductivity)>0:
                FoxProductivity = FoxProductivity.to_dict(orient='records')
                return JsonResponse(FoxProductivity, safe=False)
            # return HttpResponse(FoxProductivity)
            else:
                return HttpResponse("No Data Found")
        else:
            return HttpResponse("Get Method is not allowed")
    except Exception as e:
        print("Error in FOX Data",e)
        return HttpResponse("An error occurred while processing the request.")

# @token_required
@csrf_exempt   
def globalportal(request, **kwargs):
    # try:
    if request.method == 'POST':
        weeksbefore = request.POST.get('weeksbefore')
        director = request.POST.get('director')
        performance = request.POST.get('performance')
        print("eGP HIiii")
        gp_obj = GPProductiivty()
        print("After GPProductiivty")
        GpProd = gp_obj.GpSignOffProd(weeksbefore,director,performance)
        print("ENds")
        if len(GpProd)>0:
            GpProd1 = GpProd.to_dict(orient='records')
            return JsonResponse(GpProd1, safe=False)
        else:
            return HttpResponse("No Data Found")
    else:
        return HttpResponse("Get Method is not allowed")
    # except Exception as e:
    #     print("Error in EGP Data",e)
    #     return HttpResponse("An error occurred while processing the request.")


# @token_required
@csrf_exempt   
def director(request, **kwargs):
    try:
        if request.method == 'GET':
            direc_obj = GetDirectors()
            direc = direc_obj.directorsData()
            if len(direc)>0:
                direc1 = direc.to_dict(orient='records')
                return JsonResponse(direc1, safe=False)
            else:
                return HttpResponse("No Directors Found")
        else:
            return HttpResponse("Post Method Is Not Allowed")
    except Exception as e:
        print("Error in Director Data",e)
        return HttpResponse("An error occurred while processing the request.")












