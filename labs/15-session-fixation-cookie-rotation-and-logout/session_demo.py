import secrets
sessions = {}
def login(old_sid, user):
    sessions.pop(old_sid, None)
    new_sid = secrets.token_urlsafe(24)
    sessions[new_sid] = user
    return new_sid
def logout(sid): sessions.pop(sid, None)
if __name__ == '__main__':
    sid = 'anonymous-training-id'
    new = login(sid, 'student')
    print('changed_on_login', new != sid)
    logout(new)
    print('invalidated_on_logout', new not in sessions)
