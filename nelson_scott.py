#!/usr/bin/env python
# coding: utf-8

# In[127]:


import urllib.request as urllibr
import base64


def formatCerts(user, password, url):
    """ function to retrieve the certifactes from the url using
    the username and password provided to the function.
    Then format the retrieved certificates into a .txt file.

    Args: user (str): the string user name used for authentication
    password (str): string representing the password for authentication
    url (str): string representing the url to retrieve the data from
    """

    # encodes the user name and pass for the auth
    userpass = base64.b64encode(bytes('%s:%s' % (user, password), 'ascii'))

    # makes the header for the request
    headers = {'Authorization': 'Basic %s' % userpass.decode('utf-8')}

    # makes the request object using url and header
    r = urllibr.Request(url, headers=headers)

    # gets the meta data using the request obj
    with urllibr.urlopen(r) as response:
        certs = response.read()

    # cleans the response data
    certs = certs.decode('utf-8')[18:].split(',')
    certs[0] = certs[0][:-1]
    certs[1] = certs[1][1:-1]
    certs[2] = certs[2][1:-4]

    # set variable to control the format of the output
    outfile = open('nelson_scott.crt', 'w')
    cnt = 0

    # loop through all recieved certifcates
    for cert in certs:
        # append start of cert
        outfile.write('----Begin Certificate---- \n')
        # loop through cert ensuring line does exceed 64 chars
        while len(cert) > 0:
            if(len(cert) == 1):
                # outfile write character of the cert and new line
                outfile.write(cert[0])
                outfile.write(' \n')
                cert = cert[1:]

                # reset counter
                cnt = 0
            elif(cnt < 63):
                # outfile write character of the certificate
                outfile.write(cert[0])
                cert = cert[1:]

                # increment the counter
                cnt += 1
            else:
                # outfile write character of the cert and new line
                outfile.write(cert[0])
                outfile.write('\n')
                cert = cert[1:]

                # reset the counter
                cnt = 0

        # append end of cert to outfile
        outfile.write('----End Certificate----')
        outfile.write(' \n')

    # close the outfile
    outfile.close()


# establish the user name and password to acess data
user = 'testuser'
password = 'T3st9paS$w0rd!'

# establish url to retrieve the data from
url = 'http://test-api-app-apptest.k-apps.osh.massopen.cloud/api/v1/'
url += 'get-example-certificates'

# call the function using our params we just set
formatCerts(user, password, url)
