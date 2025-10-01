import argparse
import requests
import sys

DEFAULT_URL = "http://localhost:8000"

def create_task(args):
    payload = {"title": args.title}
    if args.description:
        payload["description"] = args.description
    if args.status:
        payload["status"] = args.status
    r = requests.post(f"{args.url}/tasks", json=payload)
    print_response(r)

def list_tasks(args):
    r = requests.get(f"{args.url}/tasks")
    print_response(r)

def get_task(args):
    r = requests.get(f"{args.url}/tasks/{args.id}")
    print_response(r)

def update_task(args):
    payload = {}
    if args.title: payload["title"] = args.title
    if args.description is not None: payload["description"] = args.description
    if args.status: payload["status"] = args.status
    r = requests.put(f"{args.url}/tasks/{args.id}", json=payload)
    print_response(r)

def delete_task(args):
    r = requests.delete(f"{args.url}/tasks/{args.id}")
    print_response(r)

def print_response(r):
    try:
        data = r.json()
    except ValueError:
        print(f"HTTP {r.status_code} - {r.text}")
        return
    print(f"HTTP {r.status_code}")
    from json import dumps
    print(dumps(data, indent=2, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description="CLI client for To-Do server")
    parser.add_argument("--url", default=DEFAULT_URL, help="Base URL of server")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list")
    p_list.set_defaults(func=list_tasks)

    p_create = sub.add_parser("create")
    p_create.add_argument("title")
    p_create.add_argument("--description", "-d", default=None)
    p_create.add_argument("--status", "-s", default=None)
    p_create.set_defaults(func=create_task)

    p_get = sub.add_parser("get")
    p_get.add_argument("id", type=int)
    p_get.set_defaults(func=get_task)

    p_update = sub.add_parser("update")
    p_update.add_argument("id", type=int)
    p_update.add_argument("--title", default=None)
    p_update.add_argument("--description", default=None)
    p_update.add_argument("--status", default=None)
    p_update.set_defaults(func=update_task)

    p_delete = sub.add_parser("delete")
    p_delete.add_argument("id", type=int)
    p_delete.set_defaults(func=delete_task)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)
    args.func(args)

if __name__ == "__main__":
    main()
