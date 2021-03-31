{'query': 
    {'bool': {
        'must': [
            {'bool': {
                'should': [
                        {'wildcard': {'comment': '*된장*'}},
                        {'wildcard': {'comment': '*찌개*'}}
                        ]
                    }
            },
            {'bool': {
                'should': [
                        {'wildcard': {'comment': '*토시*'}},
                        {'wildcard': {'comment': '*살*'}}
                    ]
                }
            }
        ]
    }
}
}

