# Github Trending Repo Scraper

This tool allows the lookup of the currently trending repositories on Github.  A language can be entered to see trending repositories of that language, or it can be left blank for trending repositories of all languages.

Output can be saved to either a txt or json file.

#

## Example Outputs


output.txt



```text

cloudflare/capnweb: TypeScript  *1,779 
elastic/elasticsearch: Java  *74,319 
LadybirdBrowser/ladybird: C++  *48,582 
HKUDS/RAG-Anything: Python  *5,552 
ultralytics/ultralytics: Python  *46,047 
istio/istio: Go  *37,359 
gin-gonic/gin: Go  *84,971 
freqtrade/freqtrade: Python  *42,955 
bytedance/Dolphin: Python  *6,450 
aliasrobotics/cai: Python  *4,229 
Gar-b-age/CookLikeHOC: JavaScript  *17,960 
mtdvio/every-programmer-should-know: Unknown  *91,707 
solana-labs/solana: Rust  *14,484 
siyuan-note/siyuan: TypeScript  *37,737 
django/django: Python  *85,152 
ByteByteGoHq/system-design-101: Unknown  *76,859 
exo-explore/exo: Python  *31,220 


```

#

output.json

```json

[
    {
        "name": "solana-labs",
        "author": "solana",
        "language": "Rust",
        "star_count": "14,484"
    },
    {
        "name": "bevyengine",
        "author": "bevy",
        "language": "Rust",
        "star_count": "42,314"
    },
    {
        "name": "rathole-org",
        "author": "rathole",
        "language": "Rust",
        "star_count": "11,838"
    },
    {
        "name": "astral-sh",
        "author": "ruff",
        "language": "Rust",
        "star_count": "42,614"
    },
    {
        "name": "BoundaryML",
        "author": "baml",
        "language": "Rust",
        "star_count": "5,986"
    },
    {
        "name": "GraphiteEditor",
        "author": "Graphite",
        "language": "Rust",
        "star_count": "21,600"
    },
    {
        "name": "iced-rs",
        "author": "iced",
        "language": "Rust",
        "star_count": "27,686"
    },
    {
        "name": "slint-ui",
        "author": "slint",
        "language": "Rust",
        "star_count": "20,421"
    },
    {
        "name": "mediar-ai",
        "author": "terminator",
        "language": "Rust",
        "star_count": "956"
    },
    {
        "name": "FuelLabs",
        "author": "sway",
        "language": "Rust",
        "star_count": "62,132"
    },
    {
        "name": "rustdesk",
        "author": "rustdesk",
        "language": "Rust",
        "star_count": "98,792"
    },
    {
        "name": "ajeetdsouza",
        "author": "zoxide",
        "language": "Rust",
        "star_count": "30,074"
    },
    {
        "name": "block",
        "author": "goose",
        "language": "Rust",
        "star_count": "19,805"
    },
    {
        "name": "paritytech",
        "author": "polkadot-sdk",
        "language": "Rust",
        "star_count": "2,455"
    },
    {
        "name": "cloudflare",
        "author": "quiche",
        "language": "Rust",
        "star_count": "10,577"
    },
    {
        "name": "paradigmxyz",
        "author": "reth",
        "language": "Rust",
        "star_count": "5,003"
    },
    {
        "name": "apache",
        "author": "datafusion",
        "language": "Rust",
        "star_count": "7,788"
    },
    {
        "name": "aptos-labs",
        "author": "aptos-core",
        "language": "Rust",
        "star_count": "6,367"
    },
    {
        "name": "EasyTier",
        "author": "EasyTier",
        "language": "Rust",
        "star_count": "7,215"
    },
    {
        "name": "typst",
        "author": "typst",
        "language": "Rust",
        "star_count": "45,739"
    },
    {
        "name": "DioxusLabs",
        "author": "dioxus",
        "language": "Rust",
        "star_count": "30,632"
    },
    {
        "name": "apache",
        "author": "arrow-rs",
        "language": "Rust",
        "star_count": "3,140"
    },
    {
        "name": "lancedb",
        "author": "lance",
        "language": "Rust",
        "star_count": "5,415"
    }
]

```

Contributions and suggestions always welcome!

Made by Kayden Ireland