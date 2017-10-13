ROLE = {
    'admin': 1,
    'booth': 3,
    'speaker': 4,
    'ambassador': 6,
    'user': 7,
    'partner': 8
}

SLOT = {
	'community': 400,
	'commercial': 3600
}

EVENT_TYPES = {
    'discuss panel',
    'speaker',
    'hackaton',
    'other'
}

EVENT_DATES = {
    '1': '2017-11-21',
    '2': '2017-11-22',
    '3': '2017-11-23'
}

SPONSOR_STAGES = {
    '1': 'lead',
    '2': 'prospect',
    '3': 'official'
}

SPONSOR_TYPES = {
    '1': 'diamond',
    '2': 'platinum',
    '3': 'gold',
    '4': 'silver'
}

VA_NUMBER = {
    'bca': '877800',
    'permata': '431800',
    'mandiri_bill': '242801',
    'bni': '119800'
}

PAYPAL = {
    'mode': "sandbox",
    'client_id': "ASPYNQMNEqYGkjNZ1nWG-MK8fB3qWgohghF0-o2POgl79_VRzUvxzu5Gy40htA1Jjt-f_iMUJ8iS2NAI",
    'client_secret': "EIIT0Y9MnxArXnYCEVSMoXBoit8rwK00eYxTjPB0v2fGhqkjJ9eLUsvyB2n4tQjUVpgujul8-99wlYnS",
    'payee': 'shi77.andy-facilitator@gmail.com',
    'return_url': 'http://localhost:5000/payment/execute',
    'cancel_url': 'http://localhost:5000/'
}

MIDTRANS_API_BASE_URL = 'https://api.sandbox.midtrans.com/v2/'
# Change these consts to devsummit later
MERCHANT_ID = 'M1066775'
CLIENT_KEY = 'VT-client-g8cB-IVLwe64YIdv'
SERVER_KEY = 'VT-server-njhqghnFUZbtZgOg9ldNtY0l:'
IMAGE_QUALITY = 70

# FCM key
FCM_SERVER_KEY = 'key=AAAA8iNOby4:APA91bGxdjtV_YTm3FnvjUiGJPPartTvM5COQFsubP-kBGP0AbmGBml1WtbYgAKc2-CDNcFGYLl4j0JzJq4AzeZwc47aURd3MTKLW_bLS6FtYokJdgjJcE7rM-9KiPlPJ029S9ua7OUF'
FCM_GENERAL_TOPIC = '/topics/devsummit_indonesia_2017'