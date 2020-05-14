CORRECT_PAYLOAD_MESSAGE1 = {
    "id": 9999,
    "wuevent": "TEST",
    "mt": "ps",
    "di": [
        {"dt": 128, "fv": "4.9B", "hv": 0},
        {"dt": 129, "fv": "10", "hv": 0},
        {"dt": 130, "fv": "3.2", "hv": 0},
        {"dt": 132, "fv": "08.49", "hv": 0},
    ],
    "ic": "8935103196301291333",
    "p": [
        {
            "location": {
                "source": "gps",
                "timestamp": "20191217 080827",
                "latitude": 51.597180,
                "longitude": 4.740835,
                "altitude": -18.699999,
                "speed": 0.196,
                "heading": 0.20,
                "satellites": 6,
                "dop": {"horizontal": 1.62, "vertical": 0.00, "time": 0.00},
                "stddev": {"latitude": 27.00, "longitude": 26.00, "altitude": 91.00},
                "motion": "U",
            }
        }
    ],
    "s": [
        {
            "n": "testLU18_B",
            "di": [{"dt": 7, "fv": "2.1", "hv": 768}],
            "ts": "20191217 080826",
            "sh": {"i": 30, "ss": [[65535]]},
        },
        {
            "n": "IM17WT07330",
            "di": [{"dt": 2, "fv": "2.2", "hv": 4112}],
            "ts": "20191217 080826",
            "sh": {"i": 30, "ss": [[216]]},
        },
    ],
    "log": "abd",
}

CORRECT_PAYLOAD_MESSAGE2 = {
    "blog": "899777076099661",
    "version": 3,
    "connection": 0,
    "msg_id": 1234,
    "wake_up_event": "wer",
    "blog_info": "fghgffhgf",
    "blog_info": "ghgfhgfhfgh",
    "message_type": "ps",
    "iccid": "8888803196301291333",
    "location": "hgfhfg",
    "log": "434324",
    "ack": "1",
    "config": "1234",
}

CORRECT_POST_RESPONSE = {
    "Success!": {
        "status_code": 201,
        "id": 1,
        "payload": {
            "blog": "899777076099661",
            "version": 3,
            "connection": 0,
            "msg_id": 2337,
            "wake_up_event": "wer",
            "blog_info": "fghgffhgf",
            "blog_info": "ghgfhgfhfgh",
            "message_type": "ps",
            "iccid": "8935103196301291333",
            "location": "hgfhfg",
            "log": "434324",
            "ack": "1",
            "config": "1234",
        },
    }
}


INCORRECT_JSON_MESSAGES = {
    "msg_id": "2337",
    "wake_up_event": "wer",
    "message_type": "ps",
    "blog_info": "fghgffhgf",
    "iccid": "8935103196301291333",
    "location": "hgfhfg",
    "blog_info": "ghgfhgfhfgh",
    "blog": "899777076099661",
    "version": "003",
    "connection1": "0",
    "ack": "1",
    "log": "434324",
    "config": "1234",
}

GET_READ_MESSAGE = {
    "blog": "123021245685956",
    "version": 0,
    "connection": -1,
    "msg_id": 2337,
    "wake_up_event": "wer",
    "blog_info": "fghgffhgf",
    "blog_info": "ghgfhgfhfgh",
    "message_type": "ps",
    "iccid": "8935103196301291333",
    "location": "hgfhfg",
    "log": "434324",
    "ack": "1",
    "config": "1234",
    "id": 101,
}
