#!/usr/bin/env python3
"""Tenner's mailbox: JMAP client for crisptenner@fastmail.com.

Token lives in fastmail.txt (gitignored — this repo is public).

Usage:
  tools/mail.py inbox [N]                     # list latest N messages (default 10)
  tools/mail.py read <email_id>               # print one message
  tools/mail.py send <to> <subject> [body]    # body from arg or stdin
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.fastmail.com/jmap/"
MAIL = "urn:ietf:params:jmap:mail"
SUBMIT = "urn:ietf:params:jmap:submission"


def token():
    return (ROOT / "fastmail.txt").read_text().strip()


def call(session, method_calls):
    req = urllib.request.Request(
        session["apiUrl"],
        data=json.dumps({"using": [MAIL, SUBMIT], "methodCalls": method_calls}).encode(),
        headers={"Authorization": f"Bearer {token()}", "Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req, timeout=30))["methodResponses"]


def get_session():
    req = urllib.request.Request(API + "session", headers={"Authorization": f"Bearer {token()}"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def account_id(session):
    return session["primaryAccounts"][MAIL]


def mailbox_id(session, acct, role):
    resp = call(session, [["Mailbox/get", {"accountId": acct}, "0"]])
    for box in resp[0][1]["list"]:
        if box.get("role") == role:
            return box["id"]
    raise SystemExit(f"no mailbox with role {role}")


def cmd_inbox(session, acct, limit):
    resp = call(session, [
        ["Email/query", {"accountId": acct, "sort": [{"property": "receivedAt", "isAscending": False}],
                         "limit": limit}, "0"],
        ["Email/get", {"accountId": acct, "#ids": {"resultOf": "0", "name": "Email/query", "path": "/ids"},
                       "properties": ["id", "receivedAt", "from", "subject", "preview"]}, "1"],
    ])
    for e in resp[1][1]["list"]:
        frm = (e.get("from") or [{}])[0].get("email", "?")
        print(f"{e['id']}  {e['receivedAt']}  {frm}\n    {e.get('subject')}\n    {e.get('preview','')[:120]}")


def cmd_read(session, acct, email_id):
    resp = call(session, [["Email/get", {"accountId": acct, "ids": [email_id],
                                         "properties": ["from", "to", "receivedAt", "subject", "textBody", "bodyValues"],
                                         "fetchTextBodyValues": True}, "0"]])
    msgs = resp[0][1]["list"]
    if not msgs:
        raise SystemExit("not found")
    e = msgs[0]
    print(f"From: {e.get('from')}\nTo: {e.get('to')}\nDate: {e.get('receivedAt')}\nSubject: {e.get('subject')}\n")
    for part in e.get("textBody", []):
        print(e["bodyValues"][part["partId"]]["value"])


def cmd_send(session, acct, to, subject, body):
    identity = call(session, [["Identity/get", {"accountId": acct}, "0"]])[0][1]["list"][0]
    drafts = mailbox_id(session, acct, "drafts")
    resp = call(session, [
        ["Email/set", {"accountId": acct, "create": {"draft": {
            "mailboxIds": {drafts: True},
            "from": [{"name": "Tenner", "email": "crisptenner@fastmail.com"}],
            "to": [{"email": to}],
            "subject": subject,
            "bodyStructure": {"type": "text/plain", "partId": "1"},
            "bodyValues": {"1": {"value": body}},
        }}}, "0"],
        ["EmailSubmission/set", {"accountId": acct, "onSuccessDestroyEmail": ["#sub"],
                                 "create": {"sub": {"emailId": "#draft", "identityId": identity["id"]}}}, "1"],
    ])
    created = resp[1][1].get("created") or {}
    if "sub" not in created:
        raise SystemExit(f"send failed: {json.dumps(resp[1][1].get('notCreated'), indent=2)}")
    print(f"sent to {to}: {subject}")


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    session = get_session()
    acct = account_id(session)
    if args[0] == "inbox":
        cmd_inbox(session, acct, int(args[1]) if len(args) > 1 else 10)
    elif args[0] == "read" and len(args) == 2:
        cmd_read(session, acct, args[1])
    elif args[0] == "send" and len(args) >= 3:
        body = args[3] if len(args) > 3 else sys.stdin.read()
        cmd_send(session, acct, args[1], args[2], body)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
