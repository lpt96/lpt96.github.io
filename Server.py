#!/usr/bin/env python3
"""
server.py — a tiny local web server for testing this site.

Why you need this: browsers block a page from loading data.json when you just
double-click home-screen.html open (a security restriction on file:// pages).
Running this script serves the folder over http://localhost instead, which
fixes that.

You do NOT need this once the site is uploaded to GitHub Pages, Netlify, Vercel,
etc. — this is only for previewing changes on your own machine.

USAGE
-----
1. Make sure this file sits in the same folder as home-screen.html, data.json, etc.
2. Open a terminal in that folder.
3. Run:  python3 server.py
4. It opens http://localhost:8000/home-screen.html directly in your browser.
5. Press Ctrl+C in the terminal to stop the server when you're done.

If port 8000 is already in use, run: python3 server.py 8080
(or any other free port number)
"""

import http.server
import socketserver
import sys
import webbrowser
import os

DEFAULT_PORT = 8080
HOME_PAGE = "home-screen.html"  # the page to open automatically — update this if you rename it again


def main():
    # Allow an optional port number as the first command-line argument
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"'{sys.argv[1]}' isn't a valid port number. Using {DEFAULT_PORT} instead.")

    # Serve whichever folder this script lives in, regardless of where it's run from
    folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(folder)

    handler = http.server.SimpleHTTPRequestHandler
    # Make sure .json files are served with the right content type
    handler.extensions_map.setdefault(".json", "application/json")

    # Note: http.server's default behavior is to look for a file named exactly
    # "index.html" when someone visits "/", and show a directory listing if it
    # can't find one. Since this site's main page isn't called that, we open
    # the real filename directly instead of relying on that default.
    base_url = f"http://localhost:{port}"
    home_url = f"{base_url}/{HOME_PAGE}"

    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Serving {folder}")
            print(f"Open {home_url} in your browser")
            print("Press Ctrl+C to stop\n")
            try:
                webbrowser.open(home_url)
            except Exception:
                pass  # not a big deal if this fails, they can open it manually
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {port} is already in use. Try a different one, e.g.:")
            print(f"  python3 server.py {port + 1}")
        else:
            raise
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()