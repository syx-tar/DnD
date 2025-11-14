#!/usr/bin/env python3
import sys
import json
import secrets
import urllib.request

# ===============================
# 📚 DAFTAR GENRE & SUBGENRE
# ===============================
genres = [
  "Contemporary Fiction","Web Novel Adaptation","Alternate History","Humor","Harem","Hack and Slash","Historical Fiction","Game show","Sports Anime","Crime Noir","Fighting","Culinary","Isekai","Heist","School Life","High Fantasy","Mythpunk","Anthology","pirate","Action","Contemporary fantasy","Dystopian","Talk Show","Slice of Life","Historical","Narrative Exploration","Slice of Life (Anime)","Manhua","Superhero","Cozy Mystery","Urban Fantasy","Dieselpunk","Manga","Mythological Retelling","Contemporary literature","Children's literature","Fiction","War","Fairy Tale Retelling","Mystery","Magical Girl","Variety Show","Adventure","Fairy tale","Docuseries","Mockumentary","Sword and Sorcery","Heroic Bloodshed","Parody","Gothic Romance","Contemporary romance","Comedy","Documentary","crime fiction","Science","Puzzle Adventure","Psychological","Steampunk","Action RPG","Docudrama","Black comedy","Animation","Music","Science Fiction","Teen Drama","Horror Anime","Soap Opera","Solarpunk","Detective Comics","nude","Romantic Comedy","Children's film","Western","Sports","Thriller","porn","Experimental","Fanfiction","Psychological Horror","Tragedy","Historical drama","Crime Thriller","Josei","Ecchi","Fantasy comedy","Epic Fantasy","Graphic Novel","RPG","Reality TV","Procedural","Reverse Harem","Crossover Universe","Apocalyptic","Postmodern Fiction","Narrative","Tactical Strategy","Manhwa","Psychological Thriller","Magical Realism","Platformer","Webtoon","Idol","Romantic Thriller","Light Novel Adaptation","Romance","Action/Adventure","Survival Horror","Political Drama","Supernatural Mystery","Martial Arts","Mini-Series","Biopic","Sci-fi","Cyber Noir","Fantasy Adventure","Comedy drama","Film noir","History","Simulation","Literary Fiction","Dystopian Fiction","Supernatural","Metroidvania","Dark Fantasy","Police procedural","Paranormal Romance","Cyberpunk","Memoir","MMORPG","Gothic Horror","Drama","Suspense","Crime","Mecha","Political Fiction","Space opera","Dark Comedy","Fantasy","Sitcom","Visual Novel","Dark Academia","Stealth","Seinen","Melodrama","Wuxia","Legal Drama","Detective","Romantic drama","Medical Drama","Horror","Shojo","Science Fantasy","Noir","Satire","Superhero Comics","Gothic fiction","Disaster","JRPG","Musical","Post-Apocalyptic","Sandbox","Shonen","Cooking","Action/adventure fiction","Erotica"
  ]

# Genre yang tidak perlu country/subdivision
genres_without_location = ["Manga", "Manhwa", "Manhua", "Western", "Wuxia"]

# ===============================
# 🔧 UTILITAS
# ===============================
args = sys.argv[1:]


def has_flag(flag):
    return flag in args


def get_arg_after(flag):
    try:
        idx = args.index(flag)
        return args[idx + 1] if idx + 1 < len(args) else None
    except ValueError:
        return None


def fetch_json(url):
    with urllib.request.urlopen(url) as response:
        data = response.read().decode()
        return json.loads(data)


def random_int(min_val, max_val):
    """Versi aman seperti crypto.randomInt(min, max)"""
    return min_val + secrets.randbelow(max_val - min_val)


# ===============================
# 🌍 MODE GENRE + COUNTRY + SUBDIVISION
# ===============================
if has_flag("-g"):
    try:
        genre = genres[random_int(0, len(genres))]
        print("🎭 Random Genre Generator 🎭")
        print("----------------------------")
        print(f"Genre: {genre}")

        if genre in genres_without_location:
            print("(No country/subdivision for this genre)")
            sys.exit(0)

        if has_flag("-c") or has_flag("-sd"):
            countries_url = "https://raw.githubusercontent.com/stefangabos/world_countries/master/data/countries/en/countries.json"
            countries = fetch_json(countries_url)

            if not countries:
                print("❌ Gagal fetch data negara")
                sys.exit(1)

            country = countries[random_int(0, len(countries))]
            print(f"Country: {country['name']} ({country['alpha2']})")

            if has_flag("-sd"):
                subdivisions_url = "https://raw.githubusercontent.com/stefangabos/world_countries/master/data/subdivisions/subdivisions.json"
                subdivisions = fetch_json(subdivisions_url)

                if not subdivisions:
                    print("❌ Gagal fetch data subdivision")
                    sys.exit(1)

                matching_subdivisions = [
                    sd for sd in subdivisions if sd["country"] == country["alpha2"].upper()
                ]

                if not matching_subdivisions:
                    print("Subdivision: (Not available)")
                else:
                    subdivision = matching_subdivisions[random_int(0, len(matching_subdivisions))]
                    print(f"Subdivision: {subdivision['name']} ({subdivision['type']})")

        sys.exit(0)
    except Exception as e:
        print("❌ Error:", str(e))
        sys.exit(1)

# ===============================
# 🌎 MODE COUNTRY + SUBDIVISION SAJA
# ===============================
elif has_flag("-c"):
    try:
        countries_url = "https://raw.githubusercontent.com/stefangabos/world_countries/master/data/countries/en/countries.json"
        countries = fetch_json(countries_url)

        if not countries:
            print("❌ Gagal fetch data negara")
            sys.exit(1)

        country = countries[random_int(0, len(countries))]
        print("🌍 Random Country Generator 🌍")
        print("------------------------------")
        print(f"Country: {country['name']} ({country['alpha2']})")

        if has_flag("-sd"):
            subdivisions_url = "https://raw.githubusercontent.com/stefangabos/world_countries/master/data/subdivisions/subdivisions.json"
            subdivisions = fetch_json(subdivisions_url)

            if not subdivisions:
                print("❌ Gagal fetch data subdivision")
                sys.exit(1)

            matching_subdivisions = [
                sd for sd in subdivisions if sd["country"] == country["alpha2"].upper()
            ]

            if not matching_subdivisions:
                print("Subdivision: (Not available)")
            else:
                subdivision = matching_subdivisions[random_int(0, len(matching_subdivisions))]
                print(f"Subdivision: {subdivision['name']} ({subdivision['type']})")

        sys.exit(0)
    except Exception as e:
        print("❌ Error:", str(e))
        sys.exit(1)

# ===============================
# 🎲 MODE DICE ROLL (D&D + RANGE)
# ===============================
elif has_flag("-e"):
    nama_event = get_arg_after("-e")
    roll_arg = args[-1]

    if not nama_event or not roll_arg:
        print("❌ Penggunaan: python roll.py -e '{namaEvent}' {jumlahDadu}d{sisiAtauRange}")
        sys.exit(1)

    import re
    match = re.match(r"^(\d+)d(\d+)(?:-(\d+))?$", roll_arg)
    if not match:
        print("❌ Format salah! Gunakan format seperti: 3d6 atau 2d20-40")
        sys.exit(1)

    jumlah_dadu = int(match[1])
    sisi_min = int(match[2]) if match[3] else 1
    sisi_max = int(match[3]) if match[3] else int(match[2])

    if jumlah_dadu < 1 or sisi_max < sisi_min:
        print("❌ Nilai dadu tidak valid! Pastikan jumlah dan range benar.")
        sys.exit(1)

    def roll_dadu(min_val, max_val):
        return random_int(min_val, max_val + 1)

    hasil_roll = [roll_dadu(sisi_min, sisi_max) for _ in range(jumlah_dadu)]
    total = sum(hasil_roll)

    print("🎲 D&D Dice Roller 🎲")
    print("--------------------")
    print(f"Event : {nama_event}")
    print(f"Dadu  : {jumlah_dadu}d{match[2]}{('-' + match[3]) if match[3] else ''}")
    print(f"Range : {sisi_min}–{sisi_max}")
    print(f"Hasil : {', '.join(map(str, hasil_roll))}")
    print(f"Total : {total}")
    sys.exit(0)

# ===============================
# ⚠️ DEFAULT HELP
# ===============================
else:
    print("""
❌ Penggunaan:
  Untuk roll dadu                     : python roll.py -e '{namaEvent}' {jumlahDadu}d{sisi} atau {jumlahDadu}d{min}-{max}
  Untuk genre                         : python roll.py -g
  Untuk genre + country               : python roll.py -g -c
  Untuk genre + country + subdivision : python roll.py -g -c -sd
  Untuk country                       : python roll.py -c
  Untuk country + subdivision          : python roll.py -c -sd
""")
    sys.exit(1)
