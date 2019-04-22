#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import HTTPServer, CGIHTTPRequestHandler


if __name__ == '__main__':
    HTTPServer(('localhost', 8000), CGIHTTPRequestHandler).serve_forever()

