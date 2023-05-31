from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.template import loader
import requests
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
import json
import csv
import time
import http.client
import uuid



# Set up your Shopify API credentials
API_KEY = 'ed5002d55f7e6bb0687f3012a4df7596'
API_SECRET = 'bdc4f2b0590c85de6ed42b9f2460124c'
SHOP_DOMAIN = 'codebyedgesite.myshopify.com'
API_VERSION = '2023-01'
TOKEN = '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'


def convertor(request):
    # with open('staging/static/src/mayfair.csv') as data:
    # csvReader = csv.reader(data, delimiter=",")
    # for row in csvReader:
    # print(row)
    return HttpResponse('done')


def customiser(request):
    raise PermissionDenied()
    # Define the API endpoint you want to query
    api_endpoint = '/admin/api/{0}/products.json'.format(API_VERSION)
    # Construct the Shopify API URL
    url = 'https://{0}:{1}@{2}{3}'.format(API_KEY,
                                          API_SECRET, SHOP_DOMAIN, api_endpoint)
    # Make a GET request to the Shopify API
    headers = {'Content-Type': 'application/json',
               'X-Shopify-Access-Token': TOKEN}
    response = requests.get(url, headers=headers)
    # Check the status code of the response
    if response.status_code == 200:
        # If the response is successful, return the data
        data = response.json()
        # print(data['products'])
    else:
        # If the response is unsuccessful, raise an exception
        response.raise_for_status()
    template = loader.get_template('staging/customiser/index.html')
    context = {
        'data': data
    }
    return HttpResponse(template.render(context, request))
    return HttpResponse("This is the customiser page")


def customiseProduct(request, key):

    context = {
        'key': key
    }
    template = loader.get_template('staging/customiser/id/index.html')
    return HttpResponse(template.render(context, request))

    # api_endpoint = '/admin/api/'+API_VERSION+'/products/'+str(identity)+'.json'
    # url = 'https://{0}:{1}@{2}{3}'.format(API_KEY, API_SECRET, SHOP_DOMAIN, api_endpoint)
    # headers = {'Content-Type': 'application/json',
    #            'X-Shopify-Access-Token': TOKEN}
    # response = requests.get(url, headers=headers)
    # if response.status_code == 200:
    #     # If the response is successful, return the data
    #     data = response.json()
    #     template = loader.get_template('staging/customiser/id/index.html')
    #     context = {
    #         'data': data
    #     }
    #     return HttpResponse(template.render(context, request))
    # else:
    #     # If the response is unsuccessful, raise an exception
    #     response.raise_for_status()


def email(request):
    if (request.method == 'POST'):
        subject = 'New Customiser Request | CodeByEdge'
        message = x = json.loads(request.body.decode('utf-8'))
        message = message['body']
        fromEmail = 'customiser@codebyedge.com'
        #recipients = ['janosaudron13@gmail.com']
        recipients = ['david.evans@codebyedge.com']
        try:
            send_mail(subject, message, fromEmail, recipients)
            return HttpResponse('Success')
        except Exception as e:
            # raise a 500 error with a custom error message
            raise Exception("Email error occured!")
    else:
        return HttpResponseBadRequest("Bad Request!")


def index(request):
    raise PermissionDenied()

    # return HttpResponse("Under Construction")


def variants(request):
    if (request.method == 'POST'):
        body = json.loads(request.body.decode('utf-8'))
        productid = body['product']
        path = 'https://codebyedgesite.myshopify.com/admin/api/2023-04/products/' + \
            str(productid)+'.json'
        headers = {'Content-Type': 'application/json',
                   'X-Shopify-Access-Token': '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'}
        try:
            response = requests.get(path, headers=headers)
            return HttpResponse(json.dumps(response.json()), content_type='application/json')
        except Exception as e:
            return HttpResponse(json.dumps(str(e)), content_type='application/json')

        try:
            response = requests.get(path, headers=headers)
            # Check the status code of the response
            if response.status_code == 200:
                # If the response is successful, return the data
                data = response.json()
                return data
            else:
                # If the response is unsuccessful, raise an exception
                return HttpResponse(json.dumps(response.json()), content_type='application/json')
        except Exception as e:
            return HttpResponse(json.dumps(str(e)), content_type='application/json')

    else:
        return HttpResponseBadRequest("Bad Request!")


def variantsCreate(request):
    if (request.method == 'POST'):
        body = json.loads(request.body.decode('utf-8'))
        productid = body['productid']
        price = body['price']
        title = uuid.uuid4()
        path = 'https://codebyedgesite.myshopify.com/admin/api/2023-04/products/' + \
            str(productid)+'/variants.json'
        headers = {'Content-Type': 'application/json',
                   'X-Shopify-Access-Token': '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'}
        variant = {
            'variant': {
                'option1': str(title),
                'price': str(price),
                'inventory_policy': 'continue'
            }
        }
        try:
            response = requests.post(path, headers=headers, data=json.dumps(variant))
            return HttpResponse(json.dumps(response.json()), content_type='application/json')
        except Exception as e:
            return HttpResponse(json.dumps(str(e)), content_type='application/json')
    else:
        return HttpResponseBadRequest("Bad Request!")
