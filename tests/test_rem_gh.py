# coding=utf-8




if __name__ == '__main__':
    from vault.unittest_secret import test_token

    u = '132nd-etcher'
    r = 'unittests'
    s = GHAuthenticatedSession(test_token)
    ss = GHAuthenticatedSession(test_token)
    assert s is ss
    print(s.user.login)
    print(s.rate_limit)
    s.create_status('caribou', '036d2d3aecc993281970a9e4d3ace6c8bd25f006',
                    'success', description='wut?', context='some_test')
    s.create_status('caribou', '036d2d3aecc993281970a9e4d3ace6c8bd25f006',
                    'pending', description='wut?', context='some_test2')
    s.create_status('caribou', '036d2d3aecc993281970a9e4d3ace6c8bd25f006',
                    'failure', description='wut?', context='some_test3')
    # print(s.get_repo('EASI').source())
    # for x in s.list_own_repos():
    #     print(x.name)
    # for x in s.list_user_repos('etcher3rd'):
    #     print(x.name)
    # print(s.create_repo('api_test', 'description', auto_init=True))
    # print(s.edit_repo('api_test', new_name='caribou'))
    # s.create_pull_request('testing PR', 'etcher3rd', 'subtitle-downloader', 'description')
    # print(s.delete_repo('api_test'))

    exit(0)
    s = GHAnonymousSession()
    all = s.get_all_releases(u, r)
    for r in all:
        for a in r.assets():
            for k in a.get_all():
                print(k)
                # rel = s.get_latest_release('132nd-etcher', 'unittests')
                # rel.print_all()