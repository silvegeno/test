# Парсинг RSS
import sys
import unittest
from rss_news import parse_rss

class ParseRssTests(unittest.TestCase):
    def test_limit_returns_one_news_item(self):
        news_list = parse_rss(rss_source, 1)
        self.assertEqual(len(news_list), 1)
        self.assertEqual(
            news_list[0]["title"],
            "The Outages Are Just Getting Started",
        )

rss_source = """
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/" version="2.0">
<channel>
<title>Feed: Artificial Intelligence Latest</title>
<description>Channel Description</description>
<link>https://www.wired.com</link>
<atom:link href="https://www.wired.com/feed/tag/ai/latest/rss" rel="self" type="application/atom+xml"/>
<copyright>© Condé Nast 2026</copyright>
<language>en-US</language>
<lastBuildDate>Sun, 22 Nov 2026 10:44:21 +0000</lastBuildDate>
<item>
<title>The Outages Are Just Getting Started</title>
<link>https://www.wired.com/story/brace-yourself-for-years-of-outage-chaos/</link>
<guid isPermaLink="false">6aff54f5dedf491d3bbcabcb</guid>
<pubDate>Sat, 21 Nov 2026 13:00:00 +0000</pubDate>
<media:content/>
<description>AI is forcing companies to patch their systems faster as attackers race to exploit newly discovered vulnerabilities. Welcome to internet outage hell.</description>
<category>Security</category>
<category>Security / Cyberattacks and Hacks</category>
<media:keywords>Kernel Panic, artificial intelligence, agentic AI, cybersecurity, Internet, security, software, Microsoft, apple, banks, NSA</media:keywords>
<dc:creator>Lily Hay Newman, Matt Burgess</dc:creator>
<dc:publisher>Condé Nast</dc:publisher>
<dc:subject>Kernel Panic</dc:subject>
<media:thumbnail url="https://media.wired.com/photos/6b00ba06fb286bb31d23be2b/master/pass/Kernel-Panic-Brace-for-More-Outages-Security.jpg" width="1232" height="1232"/>
</item>
<item>
<title>Cops Are Pushing Extremely Corny ‘Grand Theft Auto 6’ Slop</title>
<link>https://www.wired.com/story/cops-are-being-extremely-corny-about-gta-vi/</link>
<guid isPermaLink="false">6b0083c47020ceeb47169e93</guid>
<pubDate>Fri, 20 Nov 2026 23:24:02 +0000</pubDate>
<media:content/>
<description>The blockbuster game makes no secret of its contempt for law enforcement. Real police departments using it to recruit new members and scold the public apparently didn’t get the memo.</description>
<category>Culture</category>
<category>Culture / Video Games</category>
<media:keywords>Police, video games, Military, politics, Social Media, artificial intelligence, Rockstar Games</media:keywords>
<dc:creator>Miles Klee</dc:creator>
<dc:publisher>Condé Nast</dc:publisher>
<dc:subject>Right to Jail</dc:subject>
<media:thumbnail url="https://media.wired.com/photos/6b008734209518b1b255d3f5/master/pass/Law-Enforcement-GTA-Recruitment-Culture-Lucia_Caminos_05.jpg" width="2500" height="1406"/>
</item>
<item>
<title>Jensen Huang’s ‘Lying’ Alarmed Nvidia Board Ahead of His Resignation</title>
<link>https://www.wired.com/story/jensen-huangs-lying-alarmed-nvidia-board-ahead-of-his-resignation/</link>
<guid isPermaLink="false">6b006eaa6873ef9746910ed7</guid>
<pubDate>Fri, 20 Nov 2026 19:52:21 +0000</pubDate>
<media:content/>
<description>Amid allegations of multiple affairs, including with a direct report and an alleged Chinese intelligence asset, sources tell WIRED the Nvidia board’s main issue was the former CEO’s “lack of candor.”</description>
<category>Business</category>
<category>Business / Big Tech</category>
<media:keywords>Jensen Huang, NVIDIA, espionage, chips, artificial intelligence</media:keywords>
<dc:creator>Lauren Goode, Paresh Dave</dc:creator>
<dc:publisher>Condé Nast</dc:publisher>
<dc:subject>Board Games</dc:subject>
<media:thumbnail url="https://media.wired.com/photos/6b007b4f6873ef9746910ee1/master/pass/GettyImages-2298479100.jpg" width="1024" height="682"/>
</item>
</channel>
</rss>
"""

if __name__ == "__main__":
    unittest.main()

    