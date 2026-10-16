"""Collect a text-only corpus of public Reddit posts/comments via RSS feeds.

Why this exists
---------------
Reddit's unauthenticated JSON API returns 403, but the public RSS (Atom) feeds
still work. This script downloads those feeds, keeps only entries that are
plain text, and writes them to a CSV that can be hand-labeled for the project.

What it keeps / drops
---------------------
An entry is DROPPED if its body is:
  - empty (typical for link-only and image-only posts)
  - contains a link (an <a> tag or an http(s):// / www. URL)
  - contains an image, video or iframe
  - contains an emoji (in the title or body)
Duplicates (same Reddit id) are removed.

Rate limiting
-------------
Reddit answers 429 when requests come too fast. The script pauses between
requests (--delay) and waits (--backoff) before retrying after a 429/503.
Only public feeds are read; nothing here logs in to Reddit.

Usage examples
--------------
  # posts from several subreddits, hot + new, up to 2 pages each
  python3 collect_reddit_rss_text_corpus.py \
      --subreddits cybersecurity AskNetsec cybersecurity_help \
      --sorts hot new --pages 2 --out cybersecurity_posts_clean.csv

  # recent comments from one subreddit
  python3 collect_reddit_rss_text_corpus.py \
      --subreddits SecurityCareerAdvice --kind comments \
      --out securitycareeradvice_comments_clean.csv

Output CSV columns: id, type, subreddit, title, text, url
(title is blank for comments).
"""

import argparse
import csv
import html
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ATOM = {"a": "http://www.w3.org/2005/Atom"}
USER_AGENT = "Mozilla/5.0 (Macintosh) personal-research"
PAGE_SIZE = 100

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍←-⇿⌀-⏿]"
)
URL_IN_TEXT = re.compile(r"https?://|www\.")
BODY_HTML = re.compile(r"<!-- SC_OFF -->(.*?)<!-- SC_ON -->", re.S)


def fetch(url, backoff, retries=4):
    """Return the raw bytes at url, or None. Waits and retries on 429/503."""
    for _ in range(retries):
        print("GET", url, flush=True)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            return urllib.request.urlopen(req, timeout=30).read()
        except urllib.error.HTTPError as err:
            print("  HTTP", err.code, flush=True)
            if err.code not in (429, 503):
                return None
            time.sleep(backoff)
        except Exception as err:  # network problem: give up on this URL
            print("  ERROR", err, flush=True)
            return None
    return None


def feed_url(subreddit, kind, sort, after):
    """Build the RSS URL. sort may carry a query, e.g. 'top?t=year'."""
    if kind == "comments":
        url = f"https://www.reddit.com/r/{subreddit}/comments.rss?limit={PAGE_SIZE}"
    else:
        base, _, query = sort.partition("?")
        url = f"https://www.reddit.com/r/{subreddit}/{base}.rss?limit={PAGE_SIZE}"
        if query:
            url += "&" + query
    if after:
        url += f"&after={after}"
    return url


def clean_entry(entry):
    """Turn one Atom <entry> into a dict plus the raw body HTML."""
    title = entry.find("a:title", ATOM).text or ""
    content = entry.find("a:content", ATOM)
    raw = content.text if content is not None and content.text else ""
    match = BODY_HTML.search(raw)
    body_html = match.group(1) if match else ""
    text = html.unescape(re.sub(r"<[^>]+>", " ", body_html))
    text = re.sub(r"\s+", " ", text).strip()
    category = entry.find("a:category", ATOM)
    return {
        "id": entry.find("a:id", ATOM).text,
        "subreddit": category.get("term") if category is not None else "",
        "title": title,
        "text": text,
        "url": entry.find("a:link", ATOM).get("href"),
    }, body_html


def drop_reason(rec, body_html, kind):
    """Return why an entry must be dropped, or None to keep it."""
    if not rec["text"]:
        return "empty"
    if re.search(r"<a\s", body_html) or URL_IN_TEXT.search(rec["text"]):
        return "link"
    if re.search(r"<img|<video|<iframe", body_html):
        return "image"
    if EMOJI.search(rec["title"] + rec["text"]):
        return "emoji"
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--subreddits", nargs="+", required=True)
    p.add_argument("--kind", choices=["posts", "comments"], default="posts")
    p.add_argument("--sorts", nargs="+", default=["hot"], help="e.g. hot new 'top?t=year' (posts only)")
    p.add_argument("--pages", type=int, default=2, help="max pages of 100 per feed")
    p.add_argument("--target", type=int, default=0, help="stop once this many entries are kept (0 = no limit)")
    p.add_argument("--delay", type=float, default=30, help="seconds between requests")
    p.add_argument("--backoff", type=float, default=240, help="seconds to wait after a 429/503")
    p.add_argument("--out", required=True, help="output CSV path (must not already exist)")
    args = p.parse_args()

    kept, seen = [], set()
    dropped = {"empty": 0, "link": 0, "image": 0, "emoji": 0}
    sorts = ["new"] if args.kind == "comments" else args.sorts  # sort is ignored for comments

    for sub in args.subreddits:
        for sort in sorts:
            after = None
            for _ in range(args.pages):
                data = fetch(feed_url(sub, args.kind, sort, after), args.backoff)
                if not data:
                    break
                entries = ET.fromstring(data).findall("a:entry", ATOM)
                for entry in entries:
                    rec, body_html = clean_entry(entry)
                    if rec["id"] in seen:
                        continue
                    seen.add(rec["id"])
                    reason = drop_reason(rec, body_html, args.kind)
                    if reason:
                        dropped[reason] += 1
                    else:
                        rec["type"] = "comment" if args.kind == "comments" else "post"
                        if rec["type"] == "comment":
                            rec["title"] = ""
                        kept.append(rec)
                print(f"  {len(entries)} entries, {len(kept)} kept so far", flush=True)
                if args.target and len(kept) >= args.target:
                    break
                time.sleep(args.delay)
                if len(entries) < PAGE_SIZE:
                    break  # last page
                after = entries[-1].find("a:id", ATOM).text  # id of last entry = next page cursor
            if args.target and len(kept) >= args.target:
                break
        if args.target and len(kept) >= args.target:
            break

    if args.target:
        kept = kept[: args.target]

    with open(args.out, "x", newline="", encoding="utf-8") as f:  # "x": never overwrite
        writer = csv.writer(f)
        writer.writerow(["id", "type", "subreddit", "title", "text", "url"])
        for r in kept:
            writer.writerow([r["id"], r["type"], r["subreddit"], r["title"], r["text"], r["url"]])

    print(f"seen {len(seen)}, dropped {dropped}, kept {len(kept)} -> {args.out}")


if __name__ == "__main__":
    sys.exit(main())
