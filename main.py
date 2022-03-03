import json
import os
from itertools import islice
from pathlib import Path
from typing import List, Dict

import disnake
from disnake.ext import commands

bot = commands.Bot()
cwd = str(Path(__file__).parents[0])


def read_json(file_name: str):
    file_name = file_name if file_name.endswith(".json") else f"{file_name}.json"

    with open(os.path.join(cwd, file_name), "r") as file:
        data = json.load(file)
    return data


def write_json(file_name: str, data: Dict):
    file_name = file_name if file_name.endswith(".json") else f"{file_name}.json"
    with open(os.path.join(cwd, file_name), "w") as file:
        json.dump(data, file, indent=4)


bot.read_json = read_json
bot.write_json = write_json

rules: Dict[str, str] = bot.read_json("jemba_rules.json")
rules["callum swap"] = rules["clothes swap"]


async def autocomplete_rules(
    _, key: str
) -> List[str,]:
    """Return the rules that the user could still pick."""
    key = key.lower()
    possible_choices = [r.capitalize() for r in rules if key in r.lower()]
    if len(possible_choices) > 25:
        return []

    return possible_choices


async def autocomplete_rules_dict(_, key: str) -> Dict[str, str]:
    """Return the rules that the user could still pick."""
    key = key.lower()
    return {r.capitalize(): v for r, v in rules.items() if key in r.lower()}


@bot.slash_command(
    guild_ids=[741088737844264990],
    description="View a rule for a Jenga piece.",
)
async def rule(
    inter: disnake.CommandInteraction,
    piece: str = commands.Param(autocomplete=autocomplete_rules),
):
    value = rules[piece.casefold()]
    await inter.send(f"Piece: `{piece.capitalize()}`\nRule: {value}", ephemeral=True)


def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k: data[k] for k in islice(it, SIZE)}


def list_chunk(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


@bot.slash_command(
    guild_ids=[741088737844264990],
    description="List all the rules",
)
async def list_rules(inter: disnake.CommandInteraction):
    embeds = []
    for data in chunks(rules, 5):
        embed = disnake.Embed(description="")
        for k, v in data.items():
            embed.description += f"Piece: `{k.capitalize()}`\nRule: {v}\n"
        embeds.append(embed)

    for embeds in list_chunk(embeds, 8):
        await inter.channel.send(embeds=embeds)


@bot.slash_command(
    guild_ids=[741088737844264990],
    description="About me.",
)
async def about(inter: disnake.CommandInteraction):
    await inter.send(
        f"Jemba rules, digitalized.\nhttps://github.com/Skelmis/Jemba", ephemeral=True
    )


bot.run(os.environ["TOKEN"])
